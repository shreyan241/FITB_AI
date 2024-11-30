import secrets
from ninja import Router
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from profiles.api.schemas.auth import AuthRegister, AuthLogin, AuthResponse, SessionResponse
from profiles.utils.logger.logging_config import logger
from profiles.api.helpers.auth import redis_client
from asgiref.sync import sync_to_async
from typing import List
from profiles.api.helpers.auth import (
    store_token, 
    revoke_token,
    get_user_active_sessions
)

router = Router()

@router.post("/register", response=AuthResponse)
async def register(request, data: AuthRegister):
    """Register a new user"""
    logger.info(f"Registering new user: {data.username}")
    
    try:
        # Check if user exists
        exists = await sync_to_async(lambda: User.objects.filter(username=data.username).exists())()
        if exists:
            raise ValidationError("Username already exists")
            
        user = await sync_to_async(User.objects.create_user)(
            username=data.username,
            email=data.email,
            password=data.password
        )
        
        
        # Generate tokens
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)
        
        # Store both tokens
        await store_token(user.id, access_token, request)
        await store_token(user.id, refresh_token, request, is_refresh=True)
        
        logger.info(f"Successfully registered user: {user.id}")
        return {
            "token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
            "username": user.username
        }
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise

@router.post("/login", response=AuthResponse)
async def login(request, data: AuthLogin):
    """Login user"""
    logger.info(f"Login attempt: {data.username}")
    
    try:
        # Authenticate user
        user = await sync_to_async(authenticate)(
            username=data.username,
            password=data.password
        )
        
        if not user:
            raise ValidationError("Invalid credentials")
        
        # Generate new tokens
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)
        
        # Store both tokens
        await store_token(user.id, access_token, request)
        await store_token(user.id, refresh_token, request, is_refresh=True)
        
        logger.info(f"Successful login: {user.id}")
        return {
            "token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
            "username": user.username
        }
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise

@router.post("/logout")
async def logout(request):
    """Logout user"""
    if not request.auth:
        raise ValidationError("Not authenticated")
        
    try:
        await revoke_token(request.auth, request.user_id)
        logger.info(f"User logged out: {request.user_id}")
        return {"success": True}
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise

@router.get("/sessions", response=List[SessionResponse])
async def list_sessions(request):
    """List user's active sessions"""
    if not request.auth:
        raise ValidationError("Not authenticated")
        
    try:
        sessions = await get_user_active_sessions(request.user_id)
        return sessions
    except Exception as e:
        logger.error(f"Session list error: {str(e)}")
        raise

@router.post("/sessions/revoke-all")
async def revoke_all_sessions(request):
    """Revoke all sessions except current"""
    if not request.auth:
        raise ValidationError("Not authenticated")
        
    try:
        current_token = request.auth
        tokens = redis_client.smembers(f"user_tokens:{request.user_id}")
        
        for token in tokens:
            if token != current_token:
                await revoke_token(token, request.user_id)
                
        return {"success": True}
    except Exception as e:
        logger.error(f"Session revoke error: {str(e)}")
        raise