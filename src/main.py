import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from src.api import orders
from src.db.database import create_tables, engine
from src.core.log_config import setup_logger
from logging import getLogger


setup_logger()
logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables(engine)
    logger.info("Database tables created")
    yield
    await engine.dispose()
    logger.info("Database connection closed")


app = FastAPI(
    title="settings.PROJECT_NAME",
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


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
