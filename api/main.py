import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api.v1.auth.router import router as auth_router
from api.v1.vacancy.router import router as vacancy_router
from rpc import consume
from fastapi.responses import RedirectResponse

@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN201, ARG001
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(consume(loop))
    yield


app = FastAPI(
    title="NanoHire API",
    description="API для системы управления вакансиями и откликами",
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

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(vacancy_router)
app.include_router(api_v1_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
