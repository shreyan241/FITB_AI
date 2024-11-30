from ninja.security import HttpBearer
import redis
from django.conf import settings
from datetime import timedelta
import json
from asgiref.sync import sync_to_async
from django.utils import timezone
from profiles.models.auth import TokenLog
import hashlib

# Redis connection
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)
@sync_to_async
def hash_token(token: str) -> str:
    """Hash token for database storage"""
    return hashlib.sha256(token.encode()).hexdigest()

async def store_token(user_id: int, token: str, request=None, is_refresh: bool = False):
    """Store token in both Redis and Database"""
    expiry = settings.REFRESH_TOKEN_EXPIRY if is_refresh else settings.TOKEN_EXPIRY
    expires_at = timezone.now() + timedelta(seconds=expiry)
    
    # Redis storage
    token_data = {
        'user_id': user_id,
        'created_at': timezone.now().isoformat(),
        'is_refresh': is_refresh
    }
    
    redis_client.setex(
        f"token:{token}",
        expiry,
        json.dumps(token_data)
    )
    redis_client.sadd(f"user_tokens:{user_id}", token)
    
    # Database logging
    sync_to_async(TokenLog.objects.create)(
        user_id=user_id,
        token=hash_token(token),
        is_refresh=is_refresh,
        expires_at=expires_at,
        ip_address=request.META.get('REMOTE_ADDR') if request else None,
        user_agent=request.META.get('HTTP_USER_AGENT') if request else None
    )

@sync_to_async
def revoke_token(token: str, user_id: int):
    """Revoke token from Redis and update Database"""
    # Remove from Redis
    redis_client.delete(f"token:{token}")
    redis_client.srem(f"user_tokens:{user_id}", token)
    
    # Update Database
    sync_to_async(TokenLog.objects.filter)(
        token=hash_token(token),
        revoked_at__isnull=True
    ).update(revoked_at=timezone.now())

class AuthBearer(HttpBearer):
    @sync_to_async
    def authenticate(self, request, token):
        """Validate token"""
        token_data = redis_client.get(f"token:{token}")
        
        if not token_data:
            return None
            
        data = json.loads(token_data)
        
        if data.get('is_refresh'):
            return None
            
        request.user_id = data['user_id']
        return token

@sync_to_async
def get_user_active_sessions(user_id: int):
    """Get all active sessions for user"""
    return {
        'active_tokens': sync_to_async(TokenLog.objects.filter)(
            user_id=user_id,
            revoked_at__isnull=True,
            expires_at__gt=timezone.now()
        ).count(),
        'total_sessions': sync_to_async(TokenLog.objects.filter)(
            user_id=user_id
        ).count()
    }