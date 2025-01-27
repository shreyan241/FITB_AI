from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from profiles.models import UserProfile
from profiles.utils.logger.logging_config import logger
from ninja.security import HttpBearer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class GlobalAuth(HttpBearer):
    async def authenticate(self, request, token):
        try:
            # Verify token and get user
            user = await sync_to_async(User.objects.get)(auth_token__key=token)
            request.user = user  # Attach user to request
            return user
        except User.DoesNotExist:
            return None

async def check_auth_and_staff(request):
    """
    Check if user is authenticated and is staff.
    Raises PermissionDenied if not authenticated or not staff.
    
    Args:
        request: The HTTP request object
        
    Raises:
        PermissionDenied: If user is not authenticated or not staff
    """
    # Check authentication
    is_authenticated = await sync_to_async(lambda: request.user.is_authenticated)()
    if not is_authenticated:
        raise PermissionDenied("Authentication required")
    
    # Check staff status
    is_staff = await sync_to_async(lambda: request.user.is_staff)()
    if not is_staff:
        logger.warning(f"Non-staff access attempt by user {request.user.id}")
        raise PermissionDenied("Staff access required")

async def get_profile_with_auth_check(request, profile_id: int, action: str = "access") -> UserProfile:
    """
    Get profile and check if the user has permission to access it.
    Args:
        request: The request object containing auth user
        profile_id: The ID of the profile to check
        action: The action being performed (for error message)
    Returns:
        UserProfile: The profile if access is allowed
    Raises:
        ValidationError: If profile not found or user doesn't have permission
    """
    try:
        profile = await UserProfile.objects.select_related('user').aget(id=profile_id)
        
        # Check permissions
        is_superuser = await sync_to_async(lambda: request.user.is_superuser)()
        profile_user = await sync_to_async(lambda: profile.user)()
        
        if not (is_superuser or profile_user == request.user):
            raise ValidationError(f"You don't have permission to {action} this profile")
            
        return profile
    except UserProfile.DoesNotExist:
        raise ValidationError("Profile not found") 