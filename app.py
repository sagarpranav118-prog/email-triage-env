from fastapi import FastAPI
from env.environment import EmailEnv
from models.schemas import Action

app = FastAPI()

env = EmailEnv()


@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()


@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward.score,
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    obs = env.state()
    return obs.dict()