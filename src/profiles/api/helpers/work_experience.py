from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db import transaction
from asgiref.sync import sync_to_async
from profiles.models import WorkExperience
from profiles.utils.logger.logging_config import logger

@sync_to_async
def create_work_experience(profile, data):
    """Create a new work experience entry"""
    try:
        with transaction.atomic():
            # If this is marked as current job, unmark others
            if data.is_current:
                WorkExperience.objects.filter(user_profile=profile, is_current=True).update(is_current=False)
            
            # Create work experience entry
            work_exp = WorkExperience.objects.create(
                user_profile=profile,
                company=data.company,
                position_title=data.position_title,
                employment_type=data.employment_type,
                city=data.city,
                state=data.state,
                country=data.country,
                is_remote=data.is_remote,
                start_month=data.start_month,
                start_year=data.start_year,
                end_month=data.end_month,
                end_year=data.end_year,
                is_current=data.is_current,
                description=data.description
            )
            logger.info(f"Created work experience entry: {work_exp.id}")
            return work_exp
    except Exception as e:
        logger.error(f"Error creating work experience: {str(e)}")
        raise

@sync_to_async
def update_work_experience(profile_id: int, work_exp_id: int, data):
    """Update a work experience entry"""
    try:
        with transaction.atomic():
            # Get work experience entry
            work_exp = get_object_or_404(WorkExperience, id=work_exp_id, user_profile_id=profile_id)
            
            # If setting this as current, unmark others
            if data.is_current:
                WorkExperience.objects.filter(
                    user_profile_id=profile_id,
                    is_current=True
                ).exclude(id=work_exp_id).update(is_current=False)
            
            # Update fields
            update_dict = data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(work_exp, field, value)
            
            work_exp.save()
            logger.info(f"Updated work experience entry: {work_exp.id}")
            return work_exp
    except Exception as e:
        logger.error(f"Error updating work experience: {str(e)}")
        raise

@sync_to_async
def delete_work_experience(profile_id: int, work_exp_id: int):
    """Delete a work experience entry"""
    try:
        work_exp = get_object_or_404(WorkExperience, id=work_exp_id, user_profile_id=profile_id)
        work_exp.delete()
        logger.info(f"Deleted work experience entry: {work_exp_id}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Error deleting work experience: {str(e)}")
        raise

@sync_to_async
def get_work_experience_list(profile):
    """Get list of work experience entries for a profile"""
    try:
        return list(WorkExperience.objects.filter(user_profile=profile).order_by('-start_year', '-start_month'))
    except Exception as e:
        logger.error(f"Error getting work experience list: {str(e)}")
        raise 