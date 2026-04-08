import os
from openai import OpenAI
from env.environment import EmailEnv
from models.schemas import Action

print("FILE STARTED", flush=True)

client = OpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url=os.environ.get("API_BASE_URL")
)

def get_action_from_ai(observation):
    try:
        prompt = f"""
You are an email assistant.

Email:
Subject: {observation.subject}
Body: {observation.body}

Return ONLY:
action_type: classify/reply/escalate
content: your answer
"""

        response = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            timeout=10
        )

        text = response.choices[0].message.content.strip().lower()

        if "spam" in text:
            return Action(action_type="classify", content="spam")
        elif "urgent" in text:
            return Action(action_type="classify", content="urgent")
        elif "reply" in text:
            return Action(action_type="reply", content="We are sorry, we will help you.")
        elif "escalate" in text:
            return Action(action_type="escalate", content="escalating issue")

    except Exception as e:
        print(f"[ERROR] {e}", flush=True)

    return Action(action_type="classify", content="normal")


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

        MAX_STEPS = 2

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