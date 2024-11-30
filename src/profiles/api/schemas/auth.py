from ninja import Schema
from typing import Optional

class AuthRegister(Schema):
    username: str
    email: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "username": "testuser",
                "email": "test@example.com",
                "password": "securepass123"
            }
        }

class AuthLogin(Schema):
    username: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "username": "testuser",
                "password": "securepass123"
            }
        }

class AuthResponse(Schema):
    token: str
    refresh_token: str
    user_id: int
    username: str

class SessionResponse(Schema):
    active_tokens: int
    total_sessions: int