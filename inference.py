import os
from openai import OpenAI
from env.environment import EmailEnv
from models.schemas import Action


# ✅ Create client using hackathon env variables
client = OpenAI(
    api_key=os.environ.get("HF_TOKEN"),
    base_url=os.environ.get("https://router.huggingface.co/v1")
)


# ✅ AI action function
def get_action_from_ai(observation):
    try:
        prompt = f"""
You are an email assistant.

Email:
Subject: {observation.subject}
Body: {observation.body}

Return ONLY in this format:
action_type: classify/reply/escalate
content: your answer
"""

        response = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        text = response.choices[0].message.content.strip().lower()

        # Simple parsing
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
                content="We are sorry and will resolve your issue quickly."
            )

        elif "escalate" in text:
            return Action(action_type="escalate", content="escalating issue")

    except Exception as e:
        print(f"[ERROR] {e}", flush=True)

    # fallback (VERY IMPORTANT)
    return Action(action_type="classify", content="normal")


# ✅ Main run function with structured logs
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

        while not done:
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