from fastapi import FastAPI
from env import SentinelEnv
from models import Action, Observation, EnvState
import uvicorn

app = FastAPI(title="SentinelEnv API")
env = SentinelEnv()

@app.get("/")
def root():
    """Root endpoint for Hugging Face Spaces."""
    return {"message": "SentinelEnv API is running. Check /docs for API documentation."}

@app.get("/health")
def health_check():
    """Hugging Face Space health check endpoint."""
    return {"status": "ok"}

@app.post("/reset")
def reset(opts: dict = None):
    seed = opts.get("seed") if opts else None
    options = opts.get("options") if opts else None
    obs, info = env.reset(seed=seed, options=options)
    return {
        "observation": obs,
        "info": info
    }

@app.post("/step")
def step(action: Action):
    obs, reward, terminated, truncated, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "terminated": terminated,
        "truncated": truncated,
        "info": info
    }

@app.get("/state", response_model=EnvState)
def state():
    return env.state()

if __name__ == "__main__":
    # Port 7860 for consistency with HF Spaces configuration
    uvicorn.run(app, host="0.0.0.0", port=7860)
