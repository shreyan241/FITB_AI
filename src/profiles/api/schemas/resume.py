from pydantic import Field
from ninja import Schema
from datetime import datetime
from typing import Optional
from profiles.models.resume import MAX_TITLE_LENGTH

# File validation constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}

class ResumeBase(Schema):
    """Base schema with common fields"""
    title: str = Field(..., max_length=MAX_TITLE_LENGTH)

    class Config:
        extra = "forbid"

class ResumeCreate(ResumeBase):
    """Schema for creating a resume"""
    pass

class ResumeUpdate(Schema):
    """Schema for updating a resume"""
    title: Optional[str] = Field(None, max_length=MAX_TITLE_LENGTH)
    is_default: Optional[bool] = None

    class Config:
        extra = "forbid"

class ResumeResponse(ResumeBase):
    """Schema for resume responses"""
    id: int
    original_filename: str
    is_default: bool
    updated_at: datetime