from ninja import Router, File
from ninja.files import UploadedFile
from django.shortcuts import get_object_or_404
from django.db import transaction
from profiles.utils.logger.logging_config import logger
from typing import List
from profiles.models import UserProfile
from profiles.api.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from profiles.api.schemas.resume import ResumeCreate, ResumeResponse

router = Router()

@router.get("/me", response=ProfileResponse)
async def get_my_profile(request):
    """Get current user's profile"""
    logger.info(f"Fetching profile for user: {request.user.username}")
    profile = await get_object_or_404(UserProfile, user=request.user)
    return profile

@router.put("/me", response=ProfileResponse)
async def update_my_profile(request, data: ProfileUpdate):
    """Update current user's profile"""
    logger.info(f"Updating profile for user: {request.user.username}")
    profile = await get_object_or_404(UserProfile, user=request.user)
    
    # Update only provided fields
    for field, value in data.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    
    await profile.save()
    return profile

@router.post("/me/resume", response=ResumeResponse)
async def upload_profile_resume(
    request,
    title: str,
    file: UploadedFile = File(...)
):
    """Upload a resume to current user's profile"""
    logger.info(f"Uploading resume for user: {request.user.username}")
    
    try:
        profile = await get_object_or_404(UserProfile, user=request.user)
        
        with transaction.atomic():
            # Create resume using existing resume endpoint logic
            from .resume import upload_resume
            response = await upload_resume(
                request=request,
                data=ResumeCreate(title=title),
                file=file
            )
            
            logger.info(f"Successfully uploaded resume: {response.id}")
            return response
            
    except Exception as e:
        logger.error(f"Error uploading resume: {str(e)}")
        raise

@router.get("/me/resumes", response=List[ResumeResponse])
async def list_profile_resumes(request):
    """List all resumes for current user's profile"""
    logger.info(f"Listing resumes for user: {request.user.username}")
    
    profile = await get_object_or_404(UserProfile, user=request.user)
    resumes = await profile.resumes.all()
    return resumes 