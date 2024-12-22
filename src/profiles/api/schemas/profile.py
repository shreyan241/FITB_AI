from ninja import Schema
from typing import Optional
from datetime import date, datetime


class ProfileBase(Schema):
    """Base fields for Profile"""
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    birth_date: Optional[date] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

    class Config:
        extra = "forbid"


class ProfileCreate(ProfileBase):
    """Schema for creating a profile"""
    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone_number": "+1234567890",
                "birth_date": "1990-01-01",
                "city": "New York",
                "state": "NY",
                "country": "USA"
            }
        }

    
class ProfileUpdate(Schema):
    """Schema for updating a profile (all fields optional)"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birth_date: Optional[date] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "email": "new.email@example.com",
                "phone_number": "+1987654321"
            }
        }


class ProfileResponse(ProfileBase):
    """Schema for profile responses"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 