
from __future__ import annotations

from datetime import date as Date
from datetime import datetime, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.content import Platform

CalendarStatus = Literal["planned", "draft", "approved", "published"]


class CalendarPlanRequest(BaseModel):
    """Request to create a weekly content calendar."""

    model_config = ConfigDict(extra="forbid")

    topic: str = Field(..., min_length=3, max_length=200)
    start_date: Date | None = None


class CalendarPostCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date: Date
    topic: str = Field(min_length=3, max_length=200)
    theme: str = Field(min_length=2, max_length=100)
    platform: Platform = "linkedin"
    suggested_time: time = time(9, 0)
    content: str | None = Field(default=None, min_length=1)


class CalendarPost(BaseModel):
    """Represents one scheduled social media post."""

    model_config = ConfigDict(extra="forbid")

    date: Date
    topic: str
    theme: str
    platform: Platform = "linkedin"
    suggested_time: str = "09:00"
    status: CalendarStatus = "planned"
    content: str | None = None


class CalendarPostRead(CalendarPost):
    id: int
    created_at: datetime


class CalendarPostUpdate(BaseModel):
    """Fields that can be updated on a scheduled post."""

    model_config = ConfigDict(extra="forbid")

    date: Date | None = None
    topic: str | None = Field(default=None, min_length=3, max_length=200)
    theme: str | None = Field(default=None, min_length=2, max_length=100)
    platform: Platform | None = None
    suggested_time: str | None = Field(
        default=None,
        pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$",
    )
    content: str | None = Field(default=None, min_length=1)
    status: CalendarStatus | None = None

    @model_validator(mode="after")
    def require_update_fields(self) -> CalendarPostUpdate:
        if not any(getattr(self, field) is not None for field in self.model_fields_set):
            raise ValueError("At least one non-null field must be provided.")
        return self
