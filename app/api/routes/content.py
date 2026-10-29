from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.content import ContentIdea
from app.models.user import User
from app.schemas.content import (
    ContentIdeaCreate,
    ContentIdeaGenerate,
    ContentIdeaRead,
    ContentIdeaUpdate,
    Platform,
)
from app.services.content_service import ContentService
from app.services.openai_service import (
    AIProviderConfigurationError,
    AIProviderRequestError,
    AIProviderResponseError,
    CaptionGenerationService,
)

router = APIRouter(prefix="/content", tags=["content"])


@router.get("", response_model=list[ContentIdeaRead])
async def list_content(
    current_user: User = Depends(get_current_user),
    platform: Platform | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[ContentIdea]:
    service = ContentService(db)
    return service.list_content_ideas(
        owner_id=current_user.id,
        platform=platform,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=ContentIdeaRead, status_code=201)
async def create_content(
    payload: ContentIdeaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ContentIdea:
    service = ContentService(db)
    return service.create_content_idea(
        owner_id=current_user.id,
        topic=payload.topic,
        platform=payload.platform,
        content=payload.content,
    )


@router.post("/generate", response_model=ContentIdeaRead, status_code=201)
async def generate_content(
    payload: ContentIdeaGenerate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ContentIdea:
    try:
        content = CaptionGenerationService().generate_caption(
            topic=payload.topic,
            platform=payload.platform,
            audience=payload.audience,
        )
    except AIProviderConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except AIProviderRequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc
    except AIProviderResponseError as exc:
        raise HTTPException(
            status_code=502,
            detail="The configured AI provider could not generate content.",
        ) from exc

    return ContentService(db).create_content_idea(
        owner_id=current_user.id,
        topic=payload.topic,
        platform=payload.platform,
        content=content,
    )


@router.get("/{content_id}", response_model=ContentIdeaRead)
async def get_content(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ContentIdea:
    idea = ContentService(db).get_content_idea(current_user.id, content_id)
    if idea is None:
        raise HTTPException(status_code=404, detail="Content idea not found.")
    return idea


@router.patch("/{content_id}", response_model=ContentIdeaRead)
async def update_content(
    content_id: int,
    payload: ContentIdeaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ContentIdea:
    service = ContentService(db)
    idea = service.get_content_idea(current_user.id, content_id)
    if idea is None:
        raise HTTPException(status_code=404, detail="Content idea not found.")
    return service.update_content_idea(
        idea,
        payload.model_dump(exclude_unset=True, exclude_none=True),
    )


@router.delete("/{content_id}", status_code=204)
async def delete_content(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    service = ContentService(db)
    idea = service.get_content_idea(current_user.id, content_id)
    if idea is None:
        raise HTTPException(status_code=404, detail="Content idea not found.")
    service.delete_content_idea(idea)
    return Response(status_code=204)
