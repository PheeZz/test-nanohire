import asyncio
from contextlib import asynccontextmanager

from aio_pika import connect_robust
from aio_pika.patterns import RPC
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from fastapi.responses import RedirectResponse

from core import settings
from utils.dependencies import get_rpc
from webhook import webhook_router
from api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN201, ARG001
    loop = asyncio.get_event_loop()
    connection = await connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD,
        loop=loop,
    )
    channel = await connection.channel()
    rpc = await RPC.create(channel)
    app.state.rpc = rpc
    yield
    await rpc.close()
    await channel.close()
    await connection.close()


app = FastAPI(
    title="NanoHire HH Integration API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
    lifespan=lifespan,
)

origins = ["*"]
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["*"],
)

app.include_router(webhook_router)
app.include_router(api_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/test")
async def test_rpc(rpc=Depends(get_rpc)):
    """Тестовый эндпоинт для проверки работы RPC"""
    result = await rpc.proxy.remote_method(string="hello from RPC integration api test")
    print(result)
    return {"rpc_result": result}


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.WEB_SERVER_PORT,
        reload=True,
    )
