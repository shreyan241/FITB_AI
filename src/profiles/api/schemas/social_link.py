from typing import Optional
from ninja import Schema
from pydantic import validator, HttpUrl
from profiles.models.social_link import SocialLink

class SocialLinkBase(Schema):
    platform: str
    url: str

    @validator('platform')
    def validate_platform(cls, v):
        platforms = dict(SocialLink.PLATFORM_CHOICES)
        if v not in platforms:
            raise ValueError(f"Invalid platform. Must be one of: {', '.join(platforms.keys())}")
        return v

    @validator('url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")
        return v

class SocialLinkCreate(SocialLinkBase):
    pass

class SocialLinkUpdate(Schema):
    platform: Optional[str] = None
    url: Optional[str] = None

    @validator('platform')
    def validate_platform(cls, v):
        if v is None:
            return v
        platforms = dict(SocialLink.PLATFORM_CHOICES)
        if v not in platforms:
            raise ValueError(f"Invalid platform. Must be one of: {', '.join(platforms.keys())}")
        return v

    @validator('url')
    def validate_url(cls, v):
        if v is None:
            return v
        if not v.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")
        return v

class SocialLinkResponse(SocialLinkBase):
    id: int

    class Config:
        from_attributes = True