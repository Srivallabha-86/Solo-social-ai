
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CalendarPlanRequest(BaseModel):
    """Request to create a weekly content calendar."""

    model_config = ConfigDict(extra="forbid")

    topic: str = Field(..., min_length=3, max_length=200)
    start_date: date | None = None


class CalendarPost(BaseModel):
    """Represents one scheduled social media post."""

    model_config = ConfigDict(extra="forbid")

    date: date
    topic: str
    theme: str
    platform: str = "linkedin"
    suggested_time: str = "09:00"
    status: Literal[
        "planned",
        "draft",
        "approved",
        "published",
    ] = "planned"


class CalendarPostUpdate(BaseModel):
    """Fields that can be updated on a scheduled post."""

    model_config = ConfigDict(extra="forbid")

    topic: str | None = Field(default=None, min_length=3, max_length=200)
    platform: str | None = None
    suggested_time: str | None = None
    status: Literal[
        "planned",
        "draft",
        "approved",
        "published",
    ] | None = None
