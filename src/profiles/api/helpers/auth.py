from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from profiles.models import UserProfile
from profiles.utils.logger.logging_config import logger

async def check_auth_and_access(request, profile_id: int):
    """
    Check if user is authenticated and has access to the profile.
    Returns the profile if access is granted, raises PermissionDenied otherwise.
    
    Args:
        request: The HTTP request object
        profile_id: The ID of the profile to check access for
        
    Returns:
        UserProfile: The requested profile if access is granted
        
    Raises:
        PermissionDenied: If user is not authenticated or doesn't have access
    """
    # Check authentication
    is_authenticated = await sync_to_async(lambda: request.user.is_authenticated)()
    if not is_authenticated:
        raise PermissionDenied("Authentication required")
    
    # Get profile
    get_profile = sync_to_async(get_object_or_404)
    profile = await get_profile(UserProfile, id=profile_id)
    
    # Check if user is superuser
    is_superuser = await sync_to_async(lambda: request.user.is_superuser)()
    if is_superuser:
        return profile
    
    # Get user's profile ID
    get_user_profile = sync_to_async(lambda: getattr(request.user, 'profile', None))
    user_profile = await get_user_profile()
    
    if not user_profile or user_profile.id != profile_id:
        logger.warning(f"Unauthorized access attempt to profile {profile_id} by user {request.user.id}")
        raise PermissionDenied("You don't have permission to access this profile")
    
    return profile 