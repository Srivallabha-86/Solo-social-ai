
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ContentIdeaCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic: str = Field(..., min_length=3, max_length=200)
    platform: str = Field(default="linkedin", max_length=50)
    content: str = Field(..., min_length=10)


class ContentIdeaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic: str
    platform: str
    content: str
    created_at: datetime

