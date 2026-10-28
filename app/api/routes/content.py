from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_db
from app.schemas.content import ContentIdeaCreate, ContentIdeaRead
from app.services.content_service import ContentService

router = APIRouter(prefix="/content", tags=["content"])


@router.get("", response_model=list[ContentIdeaRead])
async def list_content(db=Depends(get_db)) -> list[ContentIdeaRead]:
    service = ContentService(db)
    return service.list_content_ideas()


@router.post("", response_model=ContentIdeaRead, status_code=201)
async def create_content(payload: ContentIdeaCreate, db=Depends(get_db)) -> ContentIdeaRead:
    service = ContentService(db)
    idea = service.create_content_idea(
        topic=payload.topic,
        platform=payload.platform,
        content=payload.content,
    )
    return idea
