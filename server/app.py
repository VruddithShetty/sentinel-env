from fastapi import FastAPI
from env import SentinelEnv
from models import ActionModel, ObservationModel, EnvState
import uvicorn

app = FastAPI(title="SentinelEnv API")
env = SentinelEnv()

@app.get("/")
def root():
    """Root endpoint for Hugging Face Spaces."""
    return {"message": "SentinelEnv API is running. Check /hub/spaces-config-reference for details."}

@app.get("/health")
def health_check():
    """Hugging Face Space health check endpoint."""
    return {"status": "ok"}

@app.get("/reset")
@app.post("/reset")
def reset(opts: dict = None):
    """Resets the environment (Supports GET and POST for maximum compatibility)."""
    seed = opts.get("seed") if opts else None
    options = opts.get("options") if opts else None
    obs, info = env.reset(seed=seed, options=options)
    return {
        "observation": obs,
        "info": info
    }

@app.post("/step")
def step(action: ActionModel):
    """Processes an action and returns the observation, reward, done status, and info."""
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state", response_model=EnvState)
def state():
    """Returns the complete internal state of the environment."""
    return env.state()

def main():
    """CLI entry point for starting the SentinelEnv server."""
    # Port 7860 is mandatory for HF Spaces configuration
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()
