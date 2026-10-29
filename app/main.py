from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.content import ContentIdea  # Register the database model

from app.models.calendar import CalendarPost

from app.api.routes.content import router as content_router
from app.api.routes.health import router as health_router
from app.api.routes.calendar import router as calendar_router
from app.core.config import settings
from app.db.session import init_db

init_db()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="AI-powered weekly social media marketing assistant for solo founders.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(content_router, prefix="/api/v1")
app.include_router(calendar_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Solo Social AI is running"}
