from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core import settings
from webhook import webhook_router
from api import api_router

app = FastAPI(
    title="NanoHire HH Integration API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
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
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running"}


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
