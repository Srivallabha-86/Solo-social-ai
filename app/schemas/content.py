
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Platform = Literal["linkedin", "x", "instagram"]


class ContentIdeaCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic: str = Field(..., min_length=3, max_length=200)
    platform: Platform = "linkedin"
    content: str = Field(..., min_length=10)


class ContentIdeaGenerate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic: str = Field(..., min_length=3, max_length=200)
    platform: Platform = "linkedin"
    audience: str = Field(default="solo founders", min_length=2, max_length=100)


class ContentIdeaUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic: str | None = Field(default=None, min_length=3, max_length=200)
    platform: Platform | None = None
    content: str | None = Field(default=None, min_length=10)

    @model_validator(mode="after")
    def require_update_fields(self) -> ContentIdeaUpdate:
        if not any(getattr(self, field) is not None for field in self.model_fields_set):
            raise ValueError("At least one non-null field must be provided.")
        return self


class ContentIdeaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic: str
    platform: str
    content: str
    created_at: datetime
