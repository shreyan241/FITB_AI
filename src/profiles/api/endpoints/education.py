from typing import Dict, List
from ninja import Router
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from profiles.api.schemas.education import (
    EducationCreate,
    EducationUpdate,
    EducationResponse
)
from profiles.api.helpers.education import (
    create_education,
    update_education,
    delete_education,
    get_education_list
)
from profiles.models import Education
from profiles.utils.logger.logging_config import logger
from profiles.api.helpers.auth import get_profile_with_auth_check
from asgiref.sync import sync_to_async

router = Router(tags=["education"])

@router.get("/{profile_id}/education", response=List[EducationResponse])
async def list_education(request, profile_id: int):
    """List all education entries for a profile"""
    logger.info(f"Fetching education entries for profile: {profile_id}")
    
    try:
        profile = await get_profile_with_auth_check(request, profile_id, "view education for")
        education_list = await get_education_list(profile)
        return [EducationResponse.from_orm(edu) for edu in education_list]
    except Exception as e:
        logger.error(f"Error fetching education list: {str(e)}")
        raise

@router.get("/{profile_id}/education/{education_id}", response=EducationResponse)
async def get_education(request, profile_id: int, education_id: int):
    """Get a specific education entry"""
    logger.info(f"Fetching education entry {education_id} for profile: {profile_id}")
    
    try:
        await get_profile_with_auth_check(request, profile_id, "view education for")
        
        # Get education entry asynchronously
        get_education = sync_to_async(get_object_or_404)
        education = await get_education(Education, id=education_id, user_profile_id=profile_id)
        
        return EducationResponse.from_orm(education)
    except Exception as e:
        logger.error(f"Error fetching education: {str(e)}")
        raise

@router.post("/{profile_id}/education", response=EducationResponse)
async def add_education(request, profile_id: int, data: EducationCreate):
    """Add a new education entry"""
    logger.info(f"Creating education entry for profile: {profile_id}")
    
    try:
        # Validate dates
        data.validate_dates()
        
        profile = await get_profile_with_auth_check(request, profile_id, "add education to")
        education = await create_education(profile, data)
        return EducationResponse.from_orm(education)
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Error creating education: {str(e)}")
        raise

@router.put("/{profile_id}/education/{education_id}", response=EducationResponse)
async def update_education_entry(
    request,
    profile_id: int,
    education_id: int,
    data: EducationUpdate
):
    """Update an education entry"""
    logger.info(f"Updating education entry {education_id} for profile: {profile_id}")
    
    try:
        await get_profile_with_auth_check(request, profile_id, "update education for")
        education = await update_education(profile_id, education_id, data)
        return EducationResponse.from_orm(education)
    except Exception as e:
        logger.error(f"Error updating education: {str(e)}")
        raise

@router.delete("/{profile_id}/education/{education_id}", response=Dict[str, bool])
async def delete_education_entry(request, profile_id: int, education_id: int):
    """Delete an education entry"""
    logger.info(f"Deleting education entry {education_id} for profile: {profile_id}")
    
    try:
        await get_profile_with_auth_check(request, profile_id, "delete education from")
        result = await delete_education(profile_id, education_id)
        return result
    except Exception as e:
        logger.error(f"Error deleting education: {str(e)}")
        raise 