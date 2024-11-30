from ninja import Router
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from profiles.models import UserProfile
from profiles.api.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from profiles.utils.logger.logging_config import logger
from asgiref.sync import sync_to_async

router = Router()

# Own profile operations
@router.get("/me", response=ProfileResponse)
async def get_my_profile(request):
    """Get current user's profile"""
    logger.info(f"Fetching profile for user: {request.user.id}")
    profile = await sync_to_async(get_object_or_404)(UserProfile, user=request.user)
    return ProfileResponse.from_orm(profile)

@router.patch("/me", response=ProfileResponse)
async def update_my_profile(request, data: ProfileUpdate):
    """Update current user's profile"""
    logger.info(f"Updating profile for user: {request.user.id}")
    try:
        profile = await sync_to_async(get_object_or_404)(UserProfile, user=request.user)
        
        for field, value in data.dict(exclude_unset=True).items():
            setattr(profile, field, value)
        
        await sync_to_async(profile.full_clean)()
        await sync_to_async(profile.save)()
        
        return ProfileResponse.from_orm(profile)
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise

@router.delete("/me")
async def delete_my_profile(request):
    """Delete current user's profile"""
    logger.info(f"Deleting profile for user: {request.user.id}")
    try:
        profile = await sync_to_async(get_object_or_404)(UserProfile, user=request.user)
        await sync_to_async(profile.delete)()
        return {"success": True}
    except Exception as e:
        logger.error(f"Error deleting profile: {str(e)}")
        raise

# View other profiles
@router.get("/{profile_id}", response=ProfileResponse)
async def get_profile(request, profile_id: int):
    """Get another user's profile"""
    logger.info(f"Fetching profile: {profile_id}")
    profile = await sync_to_async(get_object_or_404)(UserProfile, id=profile_id)
    return ProfileResponse.from_orm(profile)

# Initial profile creation
@router.post("", response=ProfileResponse)
async def create_profile(request, data: ProfileCreate):
    """Create a new profile"""
    logger.info(f"Creating profile for user: {request.user.id}")
    try:
        existing = await sync_to_async(UserProfile.objects.filter)(user=request.user).exists()
        if existing:
            raise ValidationError("Profile already exists for this user")
        
        profile = UserProfile(user=request.user)
        for field, value in data.dict().items():
            setattr(profile, field, value)
        
        await sync_to_async(profile.full_clean)()
        await sync_to_async(profile.save)()
        
        return ProfileResponse.from_orm(profile)
    except Exception as e:
        logger.error(f"Error creating profile: {str(e)}")
        raise