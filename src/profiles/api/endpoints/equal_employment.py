from typing import List
from ninja import Router
from django.core.exceptions import ValidationError
from profiles.api.schemas.equal_employment import (
    YesNoValue,
    YesNoDeclineValue,
    GenderValue,
    EthnicitiesValue,
    YesNoResponse,
    YesNoDeclineResponse,
    GenderResponse,
    EthnicitiesResponse,
    EqualEmploymentSummary,
    CompletionStatus
)
from profiles.api.helpers.equal_employment import (
    update_work_auth,
    update_ethnicities,
    update_gender,
    update_additional_info,
    get_summary,
    get_completion_status
)
from profiles.api.helpers.auth import get_profile_with_auth_check
from profiles.utils.logger.logging_config import logger

router = Router(tags=["equal-employment"])

# Work Authorization Endpoints
@router.put("/{profile_id}/equal-employment/authorized-us", response=YesNoResponse)
async def update_us_auth(request, profile_id: int, data: YesNoValue):
    """Update US work authorization"""
    try:
        await get_profile_with_auth_check(request, profile_id, "update work authorization for")
        return await update_work_auth(profile_id, 'authorized_us', data.value)
    except Exception as e:
        logger.error(f"Error updating US auth: {str(e)}")
        raise

@router.put("/{profile_id}/equal-employment/authorized-canada", response=YesNoResponse)
async def update_canada_auth(request, profile_id: int, data: YesNoValue):
    """Update Canada work authorization"""
    try:
        await get_profile_with_auth_check(request, profile_id, "update work authorization for")
        return await update_work_auth(profile_id, 'authorized_canada', data.value)
    except Exception as e:
        logger.error(f"Error updating Canada auth: {str(e)}")
        raise

@router.put("/{profile_id}/equal-employment/authorized-uk", response=YesNoResponse)
async def update_uk_auth(request, profile_id: int, data: YesNoValue):
    """Update UK work authorization"""
    try:
        await get_profile_with_auth_check(request, profile_id, "update work authorization for")
        return await update_work_auth(profile_id, 'authorized_uk', data.value)
    except Exception as e:
        logger.error(f"Error updating UK auth: {str(e)}")
        raise

@router.put("/{profile_id}/equal-employment/sponsorship", response=YesNoResponse)
async def update_sponsorship(request, profile_id: int, data: YesNoValue):
    """Update sponsorship requirement"""
    try:
        await get_profile_with_auth_check(request, profile_id, "update work authorization for")
        return await update_work_auth(profile_id, 'requires_sponsorship', data.value)
    except Exception as e:
        logger.error(f"Error updating sponsorship: {str(e)}")
        raise

# Demographics Endpoints
@router.put("/{profile_id}/equal-employment/ethnicities", response=EthnicitiesResponse)
async def update_ethnicities_endpoint(request, profile_id: int, data: EthnicitiesValue):
    """Update ethnicities"""
    try:
        await get_profile_with_auth_check(request, profile_id, "update demographics for")
        return await update_ethnicities(profile_id, data.values)
    except Exception as e:
        logger.error(f"Error updating ethnicities: {str(e)}")
        raise

@router.put("/{profile_id}/equal-employment/gender", response=GenderResponse)
async def update_gender_endpoint(request, profile_id: int, data: GenderValue):
    """Update gender"""
    try:
        await get_profile_with_auth_check(request, profile_id, "update demographics for")
        return await update_gender(profile_id, data.value)
    except Exception as e:
        logger.error(f"Error updating gender: {str(e)}")
        raise

# Additional Information Endpoints
@router.put("/{profile_id}/equal-employment/disability", response=YesNoDeclineResponse)
async def update_disability(request, profile_id: int, data: YesNoDeclineValue):
    """Update disability status"""
    try:
        await get_profile_with_auth_check(request, profile_id, "update additional information for")
        return await update_additional_info(profile_id, 'has_disability', data.value)
    except Exception as e:
        logger.error(f"Error updating disability status: {str(e)}")
        raise

@router.put("/{profile_id}/equal-employment/lgbtq", response=YesNoDeclineResponse)
async def update_lgbtq(request, profile_id: int, data: YesNoDeclineValue):
    """Update LGBTQ+ status"""
    try:
        await get_profile_with_auth_check(request, profile_id, "update additional information for")
        return await update_additional_info(profile_id, 'is_lgbtq', data.value)
    except Exception as e:
        logger.error(f"Error updating LGBTQ+ status: {str(e)}")
        raise

@router.put("/{profile_id}/equal-employment/veteran", response=YesNoDeclineResponse)
async def update_veteran(request, profile_id: int, data: YesNoDeclineValue):
    """Update veteran status"""
    try:
        await get_profile_with_auth_check(request, profile_id, "update additional information for")
        return await update_additional_info(profile_id, 'is_veteran', data.value)
    except Exception as e:
        logger.error(f"Error updating veteran status: {str(e)}")
        raise

# Utility Endpoints
@router.get("/{profile_id}/equal-employment/summary", response=EqualEmploymentSummary)
async def get_eeo_summary(request, profile_id: int):
    """Get all EEO data"""
    try:
        await get_profile_with_auth_check(request, profile_id, "view equal employment data for")
        return await get_summary(profile_id)
    except Exception as e:
        logger.error(f"Error getting EEO summary: {str(e)}")
        raise

@router.get("/{profile_id}/equal-employment/completion", response=CompletionStatus)
async def get_eeo_completion(request, profile_id: int):
    """Get completion status of EEO data"""
    try:
        await get_profile_with_auth_check(request, profile_id, "view equal employment data for")
        return await get_completion_status(profile_id)
    except Exception as e:
        logger.error(f"Error getting completion status: {str(e)}")
        raise