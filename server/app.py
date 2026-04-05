# SentinelCore - FastAPI Entry Point
from openenv.core.env_server import create_fastapi_app
from models import Action, Observation
from server.environment import SentinelCoreEnv

# FastAPI app for OpenEnv Environment Server
app = create_fastapi_app(env=SentinelCoreEnv, action_cls=Action, observation_cls=Observation)

def main():
    """CLI entry point for starting the SentinelCore server."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
