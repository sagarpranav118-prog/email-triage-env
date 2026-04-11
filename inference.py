import os
from openai import OpenAI
from env.environment import EmailEnv
from models.schemas import Action

# Initialize client (uses hackathon environment variables)
client = OpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url=os.environ.get("API_BASE_URL")
)


def get_action_from_ai(observation):
    try:
        prompt = f"""
You are an intelligent email assistant.

Analyze the email and decide:
1. Is it spam, normal, or urgent?
2. What action should be taken?

Return STRICTLY:
action_type: classify/reply/escalate
content: value

Email:
Subject: {observation.subject}
Body: {observation.body}
"""

        response = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            timeout=6
        )

        text = response.choices[0].message.content.strip().lower()

        if "classify" in text:
            if "spam" in text:
                return Action(action_type="classify", content="spam")
            elif "urgent" in text:
                return Action(action_type="classify", content="urgent")
            else:
                return Action(action_type="classify", content="normal")

        elif "reply" in text:
            return Action(
                action_type="reply",
                content="We are sorry. We will resolve your issue quickly."
            )

        elif "escalate" in text:
            return Action(action_type="escalate", content="Escalating issue")

    except Exception as e:
        print(f"[ERROR] {e}", flush=True)

    # 🔥 SMART FALLBACK (from second code)
    text = (observation.subject + " " + observation.body).lower()

    if any(word in text for word in ["win", "offer", "lottery", "prize", "free"]):
        return Action(action_type="classify", content="spam")
    elif "urgent" in text or "angry" in text:
        return Action(action_type="escalate", content="Escalating issue")
    else:
        return Action(action_type="reply", content="We will assist you.")


def run_env():
    env = EmailEnv()
    total_score = 0.0

    for i in range(3):
        task_name = f"task_{i+1}"
        print(f"[START] task={task_name}", flush=True)

        obs = env.reset()
        done = False
        step_count = 0
        task_score = 0.0

        MAX_STEPS = 2   # prevent timeout

        while not done and step_count < MAX_STEPS:
            step_count += 1

            action = get_action_from_ai(obs)
            obs, reward, done, _ = env.step(action)

            step_reward = reward.score
            task_score += step_reward

            print(f"[STEP] step={step_count} reward={step_reward}", flush=True)

        print(f"[END] task={task_name} score={task_score} steps={step_count}", flush=True)

        total_score += task_score

    return total_score


if __name__ == "__main__":
    final_score = run_env()
    print(f"Final Score: {final_score}", flush=True)