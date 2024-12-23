from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from profiles.models import UserProfile, EqualEmploymentData
from profiles.utils.logger.logging_config import logger

async def get_or_create_eeo_data(profile_id: int) -> EqualEmploymentData:
    """Get or create EEO data for a profile"""
    try:
        eeo_data = await sync_to_async(
            lambda: EqualEmploymentData.objects.get_or_create(user_profile_id=profile_id)
        )()
        return eeo_data[0]
    except Exception as e:
        logger.error(f"Error getting/creating EEO data: {str(e)}")
        raise

# Work Authorization Helpers
async def update_work_auth(profile_id: int, field: str, value: str) -> dict:
    """Update a work authorization field"""
    try:
        # Get or create EEO data
        eeo_data = await get_or_create_eeo_data(profile_id)
        
        if field not in ['authorized_us', 'authorized_canada', 'authorized_uk', 'requires_sponsorship']:
            raise ValidationError(f"Invalid field: {field}")
        
        setattr(eeo_data, field, value)
        await sync_to_async(eeo_data.full_clean)()
        await sync_to_async(eeo_data.save)()
        
        return {"value": value}
    except Exception as e:
        logger.error(f"Error updating work auth field: {str(e)}")
        raise

# Demographics Helpers
async def update_ethnicities(profile_id: int, values: list[str]) -> dict:
    """Update ethnicities"""
    try:
        # Get or create EEO data
        eeo_data = await get_or_create_eeo_data(profile_id)
        
        eeo_data.ethnicities = values
        await sync_to_async(eeo_data.full_clean)()
        await sync_to_async(eeo_data.save)()
        
        return {
            "values": values,
            "is_hispanic_latinx": eeo_data.is_hispanic_latinx
        }
    except Exception as e:
        logger.error(f"Error updating ethnicities: {str(e)}")
        raise

async def update_gender(profile_id: int, value: str) -> dict:
    """Update gender"""
    try:
        # Get or create EEO data
        eeo_data = await get_or_create_eeo_data(profile_id)
        
        eeo_data.gender = value
        await sync_to_async(eeo_data.full_clean)()
        await sync_to_async(eeo_data.save)()
        
        return {"value": value}
    except Exception as e:
        logger.error(f"Error updating gender: {str(e)}")
        raise

# Additional Information Helpers
async def update_additional_info(profile_id: int, field: str, value: str) -> dict:
    """Update an additional info field"""
    try:
        # Get or create EEO data
        eeo_data = await get_or_create_eeo_data(profile_id)
        
        if field not in ['has_disability', 'is_lgbtq', 'is_veteran']:
            raise ValidationError(f"Invalid field: {field}")
        
        setattr(eeo_data, field, value)
        await sync_to_async(eeo_data.full_clean)()
        await sync_to_async(eeo_data.save)()
        
        return {"value": value}
    except Exception as e:
        logger.error(f"Error updating additional info field: {str(e)}")
        raise

# Summary and Status Helpers
async def get_summary(profile_id: int) -> dict:
    """Get all EEO data"""
    try:
        # Get or create EEO data
        eeo_data = await get_or_create_eeo_data(profile_id)
        
        return {
            "authorized_us": eeo_data.authorized_us,
            "authorized_canada": eeo_data.authorized_canada,
            "authorized_uk": eeo_data.authorized_uk,
            "requires_sponsorship": eeo_data.requires_sponsorship,
            "ethnicities": eeo_data.ethnicities,
            "is_hispanic_latinx": eeo_data.is_hispanic_latinx,
            "gender": eeo_data.gender,
            "has_disability": eeo_data.has_disability,
            "is_lgbtq": eeo_data.is_lgbtq,
            "is_veteran": eeo_data.is_veteran
        }
    except Exception as e:
        logger.error(f"Error getting EEO summary: {str(e)}")
        raise

async def get_completion_status(profile_id: int) -> dict:
    """Get completion status of EEO data"""
    try:
        # Get or create EEO data
        eeo_data = await get_or_create_eeo_data(profile_id)
        
        # Check each section
        work_auth_fields = ['authorized_us', 'authorized_canada', 'authorized_uk', 'requires_sponsorship']
        demographics_fields = ['ethnicities', 'gender']
        additional_info_fields = ['has_disability', 'is_lgbtq', 'is_veteran']
        
        missing_fields = []
        
        # Check work auth
        work_auth_complete = all(getattr(eeo_data, field) in ['Yes', 'No'] for field in work_auth_fields)
        if not work_auth_complete:
            missing_fields.extend([f for f in work_auth_fields if getattr(eeo_data, f) not in ['Yes', 'No']])
        
        # Check demographics
        demographics_complete = (
            len(eeo_data.ethnicities) > 0 and
            eeo_data.gender in ['Male', 'Female', 'Non-Binary', 'Decline to state']
        )
        if not demographics_complete:
            if len(eeo_data.ethnicities) == 0:
                missing_fields.append('ethnicities')
            if eeo_data.gender not in ['Male', 'Female', 'Non-Binary', 'Decline to state']:
                missing_fields.append('gender')
        
        # Check additional info
        additional_info_complete = all(
            getattr(eeo_data, field) in ['Yes', 'No', 'Decline to state']
            for field in additional_info_fields
        )
        if not additional_info_complete:
            missing_fields.extend([
                f for f in additional_info_fields
                if getattr(eeo_data, f) not in ['Yes', 'No', 'Decline to state']
            ])
        
        return {
            "work_auth_complete": work_auth_complete,
            "demographics_complete": demographics_complete,
            "additional_info_complete": additional_info_complete,
            "all_complete": work_auth_complete and demographics_complete and additional_info_complete,
            "missing_fields": missing_fields
        }
    except Exception as e:
        logger.error(f"Error getting completion status: {str(e)}")
        raise