from ninja import Schema
from typing import Optional, List
from datetime import datetime
from .resume import ResumeResponse

class ProfileBase(Schema):
    first_name: str
    last_name: str
    bio: Optional[str] = None
    title: Optional[str] = None
    
    class Config:
        extra = "forbid"

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    title: Optional[str] = None
    
    class Config:
        extra = "forbid"

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    resumes: List[ResumeResponse]  # Include resumes in profile response
    updated_at: datetime 