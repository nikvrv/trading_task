from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
from src.api.ws.client import ConnectionManager

logger = logging.getLogger(__name__)

manager = ConnectionManager()
router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Message received from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")
