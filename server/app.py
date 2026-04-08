from fastapi import FastAPI
from env.environment import EmailEnv
from models.schemas import Action
import uvicorn

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
    return env.state().dict()


# ✅ REQUIRED MAIN FUNCTION
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


# ✅ REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()