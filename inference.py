from env.environment import EmailEnv
from models.schemas import Action


def get_action_from_ai(observation):
    text = (observation.subject + " " + observation.body).lower()

    # EASY → classify spam
    if "win" in text or "offer" in text or "lottery" in text:
        return Action(action_type="classify", content="spam")

    # MEDIUM → reply
    elif "damaged" in text or "broken" in text:
        return Action(
            action_type="reply",
            content="Sorry for the issue. We will replace or refund and assist you."
        )

    # HARD → urgent handling
    else:
        # Step 1 classify urgent
        if "urgent" in text or "asap" in text:
            return Action(action_type="classify", content="urgent")

        # Step 2 reply
        return Action(
            action_type="reply",
            content="Sorry, we will resolve this immediately."
        )


def run_env():
    env = EmailEnv()
    total_reward = 0.0

    for _ in range(3):
        obs = env.reset()
        done = False

        while not done:
            action = get_action_from_ai(obs)
            obs, reward, done, _ = env.step(action)

            # ✅ CORRECT FIELD
            total_reward += reward.score

    return total_reward


if __name__ == "__main__":
    score = run_env()
    print("Baseline Score:", score)