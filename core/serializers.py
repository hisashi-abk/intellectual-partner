"""
Common serializers for the core application.
"""

from ninja import Schema
from pydantic import Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class BaseResponseSchema(Schema):
    """Base response schema with common fields."""

    success: bool = True
    message: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponseSchema(BaseResponseSchema):
    """Error response schema."""

    success: bool = False
    errors: Optional[dict] = None


class PaginationSchema(Schema):
    """Pagination schema."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    total_pages: int
    total_items: int
    has_next: bool
    has_previous: bool


class TagSchema(Schema):
    """Tag schema."""

    id: UUID
    name: str
    color: str
    description: Optional[str] = None


class CategorySchema(Schema):
    """Category schema."""

    id: UUID
    name: str
    description: Optional[str] = None
    color: str
    icon: Optional[str] = None
    parent_id: Optional[UUID] = None
    full_path: str


class SubjectSchema(Schema):
    """Subject schema."""

    id: UUID
    name: str
    code: str
    color: str
    icon: Optional[str] = None
    description: Optional[str] = None
    is_active: bool


class ConcentrationLevelSchema(Schema):
    """Concentration level schema."""

    id: int
    user_id: int
    level: int = Field(ge=1, le=10)
    timestamp: datetime
    session_id: UUID
    notes: Optional[str] = None


class StudyEnvironmentSchema(Schema):
    """Study environment schema."""

    id: int
    user_id: int
    location: str
    background_music: Optional[str] = None
    lighting: str
    temperature: str
    noise_level: str
    effective_rating: int = Field(ge=1, le=5)
    timestamp: datetime


class AchievementSchema(Schema):
    """Achievement schema."""

    id: UUID
    user_id: int
    title: str
    description: str
    type: str
    points: int
    badge_icon: Optional[str] = None
    badge_color: str
    achieved_at: datetime
