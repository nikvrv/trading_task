import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from src.api import orders
from src.db.database import create_tables, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables(engine)
    yield
    await engine.dispose()


app = FastAPI(
    title="settings.PROJECT_NAME",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors(), "body": exc.body},
    )

app.include_router(orders.router, prefix="/orders", tags=["orders"])

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host='0.0.0.0',
        port=8000,
        reload=True
    )
