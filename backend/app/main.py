import logging
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.database import engine, Base
from app.api import auth, categories, reminders, history
from app.tasks.scheduler import start_scheduler, shutdown_scheduler
from app.config import get_settings
from app.logging_config import setup_logging

WEB_DIR = Path(__file__).parent.parent / "web"

Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(debug=settings.debug)
    logging.getLogger(__name__).info("Starting SmartReminder API")
    start_scheduler()
    yield
    shutdown_scheduler()


settings = get_settings()

app = FastAPI(title="SmartReminder API", version="1.0.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    status_code=429, content={"detail": "Rate limit exceeded"}
))

# CORS 配置：生产环境使用配置的来源，开发环境允许所有
cors_origins = [origin.strip() for origin in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(reminders.router)
app.include_router(history.router)


@app.get("/")
def serve_web():
    return FileResponse(WEB_DIR / "index.html")


app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")
