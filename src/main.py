import asyncio

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from src.api.endpoints import orders
from src.db.database import create_tables, engine
from src.core.log_config import setup_logger
from logging import getLogger
from src.api.ws.orders import router as websocket_router
from src.event_processor import MockOrderExecutor
from src.db.crud import event_queue
from dotenv import load_dotenv
from src.core.config import get_settings


load_dotenv()
setup_logger()
logger = getLogger(__name__)

settings = get_settings()


async def start_event_worker():
    executor = MockOrderExecutor(event_queue)
    asyncio.create_task(executor.event_worker())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables(engine)
    await start_event_worker()
    logger.info("Database tables created")
    yield
    await engine.dispose()
    logger.info("Database connection closed")


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors(), "body": exc.body},
    )


app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(websocket_router, tags=["websocket"])


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8000, reload=True)
