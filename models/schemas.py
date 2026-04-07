from pydantic import BaseModel
from typing import List, Optional


# 👀 What agent sees
class Observation(BaseModel):
    subject: str
    body: str
    history: List[str] = []


# 🎮 What agent can do
class Action(BaseModel):
    action_type: str  # "classify", "reply", "escalate"
    content: Optional[str] = None  # e.g. "spam" or reply text


# 🎁 Reward structure
class Reward(BaseModel):
    score: float
    feedback: Optional[str] = None