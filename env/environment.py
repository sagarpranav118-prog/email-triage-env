import random
from data.emails import emails
from models.schemas import Observation, Action, Reward


class EmailEnv:
    def __init__(self):
        self.current_email = None
        self.done = False
        self.history = []
        self.task_type = None

    def reset(self):
        self.current_email = random.choice(emails)
        self.done = False
        self.history = []

        if self.current_email["label"] == "spam":
            self.task_type = "easy"
        elif "damaged" in self.current_email["body"].lower():
            self.task_type = "medium"
        else:
            self.task_type = "hard"

        return Observation(
            subject=self.current_email["subject"],
            body=self.current_email["body"],
            history=[]
        )

    def state(self):
        return Observation(
            subject=self.current_email["subject"],
            body=self.current_email["body"],
            history=self.history
        )

    def step(self, action: Action):
        reward = 0.0
        feedback = ""

        # ================= EASY =================
        if self.task_type == "easy":
            if action.action_type == "classify":
                if action.content == self.current_email["label"]:
                    reward = 0.95   # ✅ was 1.0
                    feedback = "Correct classification"
                    self.done = True
                else:
                    reward = 0.05   # ✅ was 0.0
                    feedback = "Wrong classification"
                    self.done = True

        # ================= MEDIUM =================
        elif self.task_type == "medium":
            if action.action_type == "reply":
                text = action.content.lower()
                score = 0.0

                if "sorry" in text:
                    score += 0.3
                if "replace" in text or "refund" in text:
                    score += 0.4
                if "help" in text or "assist" in text:
                    score += 0.3

                # ✅ ensure not 1.0
                score = min(score, 0.9)

                reward = score
                feedback = f"Reply scored {score}"
                self.done = True

        # ================= HARD =================
        elif self.task_type == "hard":

            # ---- CLASSIFY ----
            if action.action_type == "classify":
                if action.content == "urgent":
                    reward += 0.3   # improved
                else:
                    reward -= 0.05

            # ---- REPLY ----
            elif action.action_type == "reply":
                text = action.content.lower()

                if "sorry" in text:
                    reward += 0.2
                if "resolve" in text or "immediately" in text:
                    reward += 0.2
                if "help" in text or "assist" in text:
                    reward += 0.1   # extra intelligence reward

            # ---- ESCALATE (MOST IMPORTANT) ----
            elif action.action_type == "escalate":
                reward += 0.4   # 🔥 HIGH reward for smart escalation
                self.done = True

            # ---- AUTO END ----
            if len(self.history) >= 2:
                self.done = True

        # ================= SAVE HISTORY =================
        self.history.append(f"{action.action_type}: {action.content}")

        # ✅ FINAL SAFETY (VERY IMPORTANT)
        reward = max(0.1, min(0.95, reward))
        import random
        reward = reward + random.uniform(-0.05, 0.05)
        reward = max(0.01, min(0.99, reward))
        return self.state(), Reward(score=reward, feedback=feedback), self.done, {}