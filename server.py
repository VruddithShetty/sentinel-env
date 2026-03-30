from fastapi import FastAPI
from env import SentinelEnv
from models import Action, Observation, EnvState
import uvicorn

app = FastAPI(title="SentinelEnv API")
env = SentinelEnv()

@app.get("/health")
def health_check():
    """Hugging Face Space health check endpoint."""
    return {"status": "ok"}

@app.post("/reset", response_model=Observation)
def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state", response_model=EnvState)
def state():
    return env.state()

if __name__ == "__main__":
    # Port 7860 for consistency with HF Spaces configuration
    uvicorn.run(app, host="0.0.0.0", port=7860)
