
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, HTTPException

from app.schemas.calendar import CalendarPlanRequest, CalendarPost
from app.services.calendar_service import CalendarService

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.post("/weekly", response_model=list[CalendarPost])
async def create_weekly_calendar(
    payload: CalendarPlanRequest,
) -> list[CalendarPost]:
    """Generate a seven-day social media content plan."""

    try:
        service = CalendarService()
        plan = service.build_weekly_plan(
            topic=payload.topic,
            start_date=payload.start_date or date.today(),
        )
        return [CalendarPost(**post) for post in plan]
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
