from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api.v1.auth.router import router as auth_router

app = FastAPI(
    title="NanoHire API",
    description="API для системы управления вакансиями и откликами",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
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

app.include_router(auth_router, prefix="/api/v1")


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
        port=8000,
        reload=True,
    )
