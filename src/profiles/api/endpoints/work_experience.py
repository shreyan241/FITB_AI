from typing import Dict, List
from ninja import Router
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from profiles.api.schemas.work_experience import (
    WorkExperienceCreate,
    WorkExperienceUpdate,
    WorkExperienceResponse
)
from profiles.api.helpers.work_experience import (
    create_work_experience,
    update_work_experience,
    delete_work_experience,
    get_work_experience_list
)
from profiles.models import WorkExperience
from profiles.utils.logger.logging_config import logger
from profiles.api.helpers.auth import get_profile_with_auth_check
from asgiref.sync import sync_to_async

router = Router(tags=["work experience"])

@router.get("/{profile_id}/work-experience", response=List[WorkExperienceResponse])
async def list_work_experience(request, profile_id: int):
    """List all work experience entries for a profile"""
    logger.info(f"Fetching work experience entries for profile: {profile_id}")
    
    try:
        profile = await get_profile_with_auth_check(request, profile_id, "view work experience for")
        work_exp_list = await get_work_experience_list(profile)
        return [WorkExperienceResponse.from_orm(exp) for exp in work_exp_list]
    except Exception as e:
        logger.error(f"Error fetching work experience list: {str(e)}")
        raise

@router.get("/{profile_id}/work-experience/{work_exp_id}", response=WorkExperienceResponse)
async def get_work_experience(request, profile_id: int, work_exp_id: int):
    """Get a specific work experience entry"""
    logger.info(f"Fetching work experience entry {work_exp_id} for profile: {profile_id}")
    
    try:
        await get_profile_with_auth_check(request, profile_id, "view work experience for")
        
        # Get work experience entry asynchronously
        get_work_exp = sync_to_async(get_object_or_404)
        work_exp = await get_work_exp(WorkExperience, id=work_exp_id, user_profile_id=profile_id)
        
        return WorkExperienceResponse.from_orm(work_exp)
    except Exception as e:
        logger.error(f"Error fetching work experience: {str(e)}")
        raise

@router.post("/{profile_id}/work-experience", response=WorkExperienceResponse)
async def add_work_experience(request, profile_id: int, data: WorkExperienceCreate):
    """Add a new work experience entry"""
    logger.info(f"Creating work experience entry for profile: {profile_id}")
    
    try:
        # Validate dates
        data.validate_dates()
        
        profile = await get_profile_with_auth_check(request, profile_id, "add work experience to")
        work_exp = await create_work_experience(profile, data)
        return WorkExperienceResponse.from_orm(work_exp)
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise ValidationError(str(e))
    except Exception as e:
        logger.error(f"Error creating work experience: {str(e)}")
        raise

@router.put("/{profile_id}/work-experience/{work_exp_id}", response=WorkExperienceResponse)
async def update_work_experience_entry(
    request,
    profile_id: int,
    work_exp_id: int,
    data: WorkExperienceUpdate
):
    """Update a work experience entry"""
    logger.info(f"Updating work experience entry {work_exp_id} for profile: {profile_id}")
    
    try:
        await get_profile_with_auth_check(request, profile_id, "update work experience for")
        work_exp = await update_work_experience(profile_id, work_exp_id, data)
        return WorkExperienceResponse.from_orm(work_exp)
    except Exception as e:
        logger.error(f"Error updating work experience: {str(e)}")
        raise

@router.delete("/{profile_id}/work-experience/{work_exp_id}", response=Dict[str, bool])
async def delete_work_experience_entry(request, profile_id: int, work_exp_id: int):
    """Delete a work experience entry"""
    logger.info(f"Deleting work experience entry {work_exp_id} for profile: {profile_id}")
    
    try:
        await get_profile_with_auth_check(request, profile_id, "delete work experience from")
        result = await delete_work_experience(profile_id, work_exp_id)
        return result
    except Exception as e:
        logger.error(f"Error deleting work experience: {str(e)}")
        raise 