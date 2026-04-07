from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
import uvicorn
import json
import os
import sys
from typing import Dict, Any

# Root imports
from env import SentinelCoreEnv
from models import Action, Observation

app = FastAPI(
    title="SentinelCore OpenEnv Server",
    description="Behavioral safety evaluation platform for agentic AI.",
    version="1.0.0"
)

env = SentinelCoreEnv()

@app.get("/")
async def root():
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")

@app.get("/metadata")
async def get_metadata():
    """Returns OpenEnv compliant metadata."""
    return {
        "name": "SentinelCore",
        "description": "Safety evaluation platform for agentic AI. Validates behavior against DevOps, SRE, and adversarial scenarios.",
        "version": "1.0.0",
        "author": "SentinelCore Team",
        "spec_version": "1.0"
    }

@app.post("/reset")
async def reset():
    """Gymnasium-style reset endpoint."""
    obs, info = env.reset()
    return {
        "observation": obs.model_dump(),
        "info": info
    }

@app.post("/step")
async def step(action_data: Dict[str, Any]):
    """Gymnasium-style step endpoint returning a 5-tuple payload."""
    try:
        action = Action(**action_data)
        obs, reward, terminated, truncated, info = env.step(action)
        return {
            "observation": obs.model_dump(),
            "reward": reward,
            "terminated": terminated,
            "truncated": truncated,
            "info": info
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/state")
async def get_state():
    """Returns the current internal state."""
    return env.state()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """OpenEnv V1.0 WebSocket Interface."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            msg_type = message.get("type")
            
            if msg_type == "reset":
                obs, info = env.reset()
                await websocket.send_json({
                    "type": "observation",
                    "data": obs.model_dump(),
                    "info": info
                })
            elif msg_type == "step":
                action_data = message.get("data", {})
                action = Action(**action_data)
                obs, reward, terminated, truncated, info = env.step(action)
                await websocket.send_json({
                    "type": "step_result",
                    "data": {
                        "observation": obs.model_dump(),
                        "reward": reward,
                        "terminated": terminated,
                        "truncated": truncated,
                        "info": info
                    }
                })
            elif msg_type == "state":
                await websocket.send_json({
                    "type": "state",
                    "data": env.state()
                })
                
    except WebSocketDisconnect:
        print("Client disconnected")

def main():
    """CLI entry point for starting the SentinelCore server."""
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
