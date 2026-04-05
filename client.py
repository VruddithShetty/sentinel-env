import websockets
import json
import asyncio
from typing import Dict, Any

class SentinelClient:
    """
    WebSocket client for OpenEnv V1.0 compliance.
    """
    def __init__(self, url: str):
        # OpenEnv core expects WebSocket at /ws path
        url = url.rstrip("/")
        if not url.endswith("/ws"):
            url += "/ws"
        self.url = url.replace("http://", "ws://").replace("https://", "wss://")
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.url)

    async def reset(self) -> Dict[str, Any]:
        """Resets the environment and returns initial observation."""
        message = {"type": "reset"}
        await self.websocket.send(json.dumps(message))
        response = await self.websocket.recv()
        return json.loads(response)

    async def step(self, action_text: str) -> Dict[str, Any]:
        """Submits an action and returns updated observation/reward."""
        message = {
            "type": "step",
            "action": {"text": action_text}
        }
        await self.websocket.send(json.dumps(message))
        response = await self.websocket.recv()
        return json.loads(response)

    async def close(self):
        if self.websocket:
            await self.websocket.close()
