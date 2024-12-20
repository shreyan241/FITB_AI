from typing import Dict, List
from ninja import Router, File, Form
from ninja.files import UploadedFile
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from profiles.api.helpers.resume import (
    check_profile_access,
    create_or_update_resume,
    delete_resume_and_update_default,
    get_profile_default_resume,
    set_resume_as_default,
    validate_resume_file,
)
from profiles.models import UserProfile
from profiles.api.schemas.resume import ResumeCreate, ResumeResponse
from profiles.models.resume import Resume
from profiles.utils.logger.logging_config import logger
from asgiref.sync import sync_to_async


router = Router()

@router.post("/{profile_id}/resumes", response=ResumeResponse)
async def upload_resume(
    request,
    profile_id: int,
    data: ResumeCreate = Form(...),
    file: UploadedFile = File(...)
):
    """Upload or update a new resume"""
    logger.info(f"Starting resume upload for file: {file.name}")
    check_profile_access(request, profile_id)
    try:
        # Get or create profile
        profile = await sync_to_async(get_object_or_404)(UserProfile, id=profile_id)
        # Validate file
        await validate_resume_file(file)
        # Create resume and save file
        resume = await create_or_update_resume(profile, data.title, file)
        logger.info(f"Successfully uploaded resume: {resume.id}")
        return ResumeResponse.from_orm(resume)
        
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise


@router.get("/{profile_id}/resumes", response=List[ResumeResponse])
async def list_resumes(request, profile_id: int):
    """List all resumes for a profile"""
    logger.info(f"Fetching resumes for profile: {profile_id}")
    check_profile_access(request, profile_id)
    # Get profile
    profile = await sync_to_async(get_object_or_404)(UserProfile, id=profile_id)
    # Get resumes
    resumes = await sync_to_async(list)(
        Resume.objects.filter(user_profile=profile).order_by('-updated_at')
    )
    return [ResumeResponse.from_orm(resume) for resume in resumes]


@router.get("/{profile_id}/resumes/{resume_id}", response=ResumeResponse)
async def get_resume(request, profile_id: int, resume_id: int):
    """Get specific resume details"""
    logger.info(f"Fetching resume {resume_id} for profile: {profile_id}")
    check_profile_access(request, profile_id)
    resume = await sync_to_async(get_object_or_404)(
        Resume, 
        id=resume_id,
        user_profile_id=profile_id
    )
    
    return ResumeResponse.from_orm(resume)


@router.delete("/{profile_id}/resumes/{resume_id}", response=Dict[str, bool])
async def delete_resume(request, profile_id: int, resume_id: int):
    """Delete a specific resume and handle default resume logic"""
    logger.info(f"Processing delete request for resume {resume_id}")
    check_profile_access(request, profile_id)
    try:
        # Check access
        check_profile_access(request, profile_id)
        # Delete resume and handle default logic
        result = await delete_resume_and_update_default(profile_id, resume_id)
        return result
    except Exception as e:
        logger.error(f"Error deleting resume {resume_id}: {str(e)}")
        raise


@router.put("/{profile_id}/resumes/{resume_id}/set-default", response=ResumeResponse)
async def set_default_resume(request, profile_id: int, resume_id: int):
    """Set a specific resume as default"""
    try:
        check_profile_access(request, profile_id)
        resume = await set_resume_as_default(profile_id, resume_id)
        return ResumeResponse.from_orm(resume)
    except Exception as e:
        logger.error(f"Error setting default resume: {str(e)}")
        raise


@router.get("/{profile_id}/resumes/default", response=ResumeResponse)
async def get_default_resume(request, profile_id: int):
    """Get the default resume"""
    try:
        check_profile_access(request, profile_id)
        resume = await get_profile_default_resume(profile_id)
        if not resume:
            raise Http404("No resume found for this profile")
        return ResumeResponse.from_orm(resume)
    except Exception as e:
        logger.error(f"Error getting default resume: {str(e)}")
        raise
