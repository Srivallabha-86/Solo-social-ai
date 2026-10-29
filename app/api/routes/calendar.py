
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.calendar import CalendarPost as CalendarPostModel
from app.models.user import User
from app.schemas.calendar import (
    CalendarPlanRequest,
    CalendarPostCreate,
    CalendarStatus,
    CalendarPostRead,
    CalendarPostUpdate,
)
from app.services.calendar_service import CalendarService

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.post("", response_model=CalendarPostRead, status_code=201)
async def create_calendar_post(
    payload: CalendarPostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CalendarPostRead:
    post = CalendarService(db).create_post(
        owner_id=current_user.id,
        post_date=payload.date,
        topic=payload.topic,
        theme=payload.theme,
        platform=payload.platform,
        suggested_time=payload.suggested_time,
        content=payload.content,
    )
    return _serialize_post(post)


@router.post("/weekly", response_model=list[CalendarPostRead])
async def create_weekly_calendar(
    payload: CalendarPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[CalendarPostRead]:
    """Generate a seven-day social media content plan."""

    try:
        service = CalendarService(db)
        posts = service.create_weekly_plan(
            owner_id=current_user.id,
            topic=payload.topic,
            start_date=payload.start_date or date.today(),
        )
        return [_serialize_post(post) for post in posts]
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


def _serialize_post(post: CalendarPostModel) -> CalendarPostRead:
    return CalendarPostRead(
        id=post.id,
        date=post.scheduled_date.date(),
        topic=post.topic,
        theme=post.theme,
        platform=post.platform,
        suggested_time=post.suggested_time,
        status=post.status,
        content=post.content,
        created_at=post.created_at,
    )


@router.get("", response_model=list[CalendarPostRead])
async def list_calendar_posts(
    current_user: User = Depends(get_current_user),
    start_date: date | None = None,
    end_date: date | None = None,
    status: CalendarStatus | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[CalendarPostRead]:
    if start_date is not None and end_date is not None and end_date < start_date:
        raise HTTPException(status_code=422, detail="end_date must be on or after start_date.")
    posts = CalendarService(db).list_posts(
        current_user.id,
        start_date,
        end_date,
        status,
        limit=limit,
        offset=offset,
    )
    return [_serialize_post(post) for post in posts]


@router.get("/{post_id}", response_model=CalendarPostRead)
async def get_calendar_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CalendarPostRead:
    post = CalendarService(db).get_post(current_user.id, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Calendar post not found.")
    return _serialize_post(post)


@router.patch("/{post_id}", response_model=CalendarPostRead)
async def update_calendar_post(
    post_id: int,
    payload: CalendarPostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CalendarPostRead:
    service = CalendarService(db)
    post = service.get_post(current_user.id, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Calendar post not found.")
    updated = service.update_post(
        post,
        payload.model_dump(exclude_unset=True, exclude_none=True),
    )
    return _serialize_post(updated)


@router.delete("/{post_id}", status_code=204)
async def delete_calendar_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    service = CalendarService(db)
    post = service.get_post(current_user.id, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Calendar post not found.")
    service.delete_post(post)
    return Response(status_code=204)
