# SentinelCore - FastAPI Entry Point
from openenv.core.env_server import create_fastapi_app
from models import Action, Observation
from server.environment import SentinelCoreEnv

# FastAPI app for OpenEnv Environment Server
app = create_fastapi_app(env=SentinelCoreEnv, action_cls=Action, observation_cls=Observation)
