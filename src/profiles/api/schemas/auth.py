from ninja import Schema
from typing import Optional

class Auth0TokenSchema(Schema):
    """Schema for Auth0 token validation request"""
    token: str

class UserResponse(Schema):
    """Schema for user response"""
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_verified: bool
    auth0_id: str

class UserRegistrationSchema(Schema):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class TokenResponse(Schema):
    token: str

class MessageResponse(Schema):
    message: str

class TokenMessageResponse(Schema):
    message: str
    token: str