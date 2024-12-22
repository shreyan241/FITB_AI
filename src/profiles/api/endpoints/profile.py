from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError, PermissionDenied
from profiles.models import UserProfile
from profiles.api.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from profiles.utils.logger.logging_config import logger
from asgiref.sync import sync_to_async
from profiles.api.helpers.auth import check_auth_and_access

router = Router(tags=["profiles"])

@router.get("/me", response=ProfileResponse)
async def get_my_profile(request):
    """Get the profile of the currently logged in user"""
    if not await sync_to_async(lambda: request.user.is_authenticated)():
        raise PermissionDenied("Authentication required")
    
    try:
        # Get or create profile for the current user
        profile = await sync_to_async(
            lambda: UserProfile.objects.get_or_create(user=request.user)[0]
        )()
        
        # Check access (this will also verify authentication)
        await check_auth_and_access(request, profile.id)
        
        return profile
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        raise ValidationError("Failed to get user profile")

@router.get("/{profile_id}", response=ProfileResponse)
async def get_profile(request, profile_id: int):
    """Get a profile by ID"""
    logger.info(f"Fetching profile: {profile_id}")
    profile = await check_auth_and_access(request, profile_id)
    return ProfileResponse.from_orm(profile)

@router.post("", response=ProfileResponse)
async def create_profile(request, data: ProfileCreate):
    """Create or update profile for authenticated user"""
    # Check authentication
    if not await sync_to_async(lambda: request.user.is_authenticated)():
        raise PermissionDenied("Authentication required")
    
    user = await sync_to_async(lambda: request.user)()
    logger.info(f"Creating/updating profile for user: {user.id}")
    
    try:
        # Get or create profile
        profile = await sync_to_async(
            lambda: UserProfile.objects.get_or_create(user=user)[0]
        )()
        
        # Update profile fields
        for field, value in data.dict().items():
            setattr(profile, field, value)
        
        await sync_to_async(profile.full_clean)()
        await sync_to_async(profile.save)()
        
        return ProfileResponse.from_orm(profile)
    except Exception as e:
        logger.error(f"Error in create_profile: {str(e)}")
        raise

@router.patch("/{profile_id}", response=ProfileResponse)
async def update_profile(request, profile_id: int, data: ProfileUpdate):
    """Update a profile"""
    logger.info(f"Updating profile: {profile_id}")
    try:
        profile = await check_auth_and_access(request, profile_id)
        
        for field, value in data.dict(exclude_unset=True).items():
            setattr(profile, field, value)
        
        await sync_to_async(profile.full_clean)()
        await sync_to_async(profile.save)()
        
        return ProfileResponse.from_orm(profile)
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise

@router.delete("/{profile_id}")
async def delete_profile(request, profile_id: int):
    """Delete a profile"""
    logger.info(f"Deleting profile: {profile_id}")
    try:
        profile = await check_auth_and_access(request, profile_id)
        await sync_to_async(profile.delete)()
        return {"success": True}
    except Exception as e:
        logger.error(f"Error deleting profile: {str(e)}")
        raise