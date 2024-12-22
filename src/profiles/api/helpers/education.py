from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db import transaction
from asgiref.sync import sync_to_async
from profiles.models import Education
from profiles.utils.logger.logging_config import logger

@sync_to_async
def create_education(profile, data):
    """Create a new education entry"""
    try:
        with transaction.atomic():
            # If this is marked as current education, unmark others
            if data.is_current:
                Education.objects.filter(user_profile=profile, is_current=True).update(is_current=False)
            
            # Create education entry
            education = Education.objects.create(
                user_profile=profile,
                school_name=data.school_name,
                degree_type=data.degree_type,
                major=data.major,
                minor=data.minor,
                start_month=data.start_month,
                start_year=data.start_year,
                end_month=data.end_month,
                end_year=data.end_year,
                is_current=data.is_current,
                gpa=data.gpa
            )
            logger.info(f"Created education entry: {education.id}")
            return education
    except Exception as e:
        logger.error(f"Error creating education: {str(e)}")
        raise

@sync_to_async
def update_education(profile_id: int, education_id: int, data):
    """Update an education entry"""
    try:
        with transaction.atomic():
            # Get education entry
            education = get_object_or_404(Education, id=education_id, user_profile_id=profile_id)
            
            # If setting this as current, unmark others
            if data.is_current:
                Education.objects.filter(
                    user_profile_id=profile_id,
                    is_current=True
                ).exclude(id=education_id).update(is_current=False)
            
            # Update fields
            update_dict = data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(education, field, value)
            
            education.save()
            logger.info(f"Updated education entry: {education.id}")
            return education
    except Exception as e:
        logger.error(f"Error updating education: {str(e)}")
        raise

@sync_to_async
def delete_education(profile_id: int, education_id: int):
    """Delete an education entry"""
    try:
        education = get_object_or_404(Education, id=education_id, user_profile_id=profile_id)
        education.delete()
        logger.info(f"Deleted education entry: {education_id}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Error deleting education: {str(e)}")
        raise

@sync_to_async
def get_education_list(profile):
    """Get list of education entries for a profile"""
    try:
        return list(Education.objects.filter(user_profile=profile).order_by('-start_year', '-start_month'))
    except Exception as e:
        logger.error(f"Error getting education list: {str(e)}")
        raise 