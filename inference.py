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

            # ✅ correct reward field
            step_reward = reward.score
            task_score += step_reward

            print(f"[STEP] step={step_count} reward={step_reward}", flush=True)

        print(f"[END] task={task_name} score={task_score} steps={step_count}", flush=True)

        total_score += task_score

    return total_score


if __name__ == "__main__":
    score = run_env()
    print(f"Final Score: {score}", flush=True)