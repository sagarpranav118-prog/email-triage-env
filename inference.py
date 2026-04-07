import os
from openai import OpenAI
from env.environment import EmailEnv
from models.schemas import Action

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "meta-llama/llama-3-8b-instruct"


def get_action_from_ai(observation):
    prompt = f"""
    You are an email assistant.

    Email:
    Subject: {observation.subject}
    Body: {observation.body}

    Decide one action:
    - classify: spam/normal/urgent
    - reply: <text>
    - escalate

    Output format:
    action_type: <type>
    content: <content>
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content

    # simple parsing
    output = output.lower()

    if "spam" in output:
        return Action(action_type="classify", content="spam")
    elif "normal" in output:
        return Action(action_type="classify", content="normal")
    elif "urgent" in output:
        return Action(action_type="classify", content="urgent")
    elif "escalate" in output:
        return Action(action_type="escalate")
    else:
        return Action(action_type="reply", content=output)


def run_env():
    env = EmailEnv()
    obs = env.reset()

    total_reward = 0

    for _ in range(5):
        action = get_action_from_ai(obs)
        obs, reward, done, _ = env.step(action)
        total_reward += reward.score

        if done:
            break

    return total_reward


if __name__ == "__main__":
    score = run_env()
    print("Baseline Score:", score)