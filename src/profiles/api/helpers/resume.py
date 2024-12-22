import os
from django.shortcuts import get_object_or_404
from ninja.files import UploadedFile
from django.core.exceptions import ValidationError
from django.db import transaction
from profiles.models import Resume
from profiles.models.resume import MAX_RESUMES_PER_USER
from profiles.api.schemas.resume import MAX_FILE_SIZE, ALLOWED_EXTENSIONS
from profiles.models.user_profile import UserProfile
from profiles.utils.logger.logging_config import logger
from asgiref.sync import sync_to_async
from uuid import uuid4
from profiles.utils.validators.text import sanitize_text


async def validate_resume_file(file: UploadedFile):
    """Validate resume file size and extension"""
    # Log file details
    logger.info(f"Validating resume file - Name: {file.name}, Size: {file.size} bytes, Content-Type: {file.content_type}")
    # Check file size
    if file.size > MAX_FILE_SIZE:
        raise ValidationError(f'File size must be no more than {MAX_FILE_SIZE/1024/1024}MB')
    # Check file extension
    _, ext = os.path.splitext(file.name.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError('File type not supported. Please upload files with extension .pdf, .doc, .docx or .txt')
    logger.info("Resume file validated successfully")

def generate_resume_s3_key(profile, title, file):
    """Generate S3 key for resume"""
    logger.info(f"Generating S3 key for resume - Profile ID: {profile.id}, Title: {title}, File Name: {file.name}")
    ext = file.name.split('.')[-1].lower()
    folder = f"user_{profile.id}"
    unique_id = str(uuid4())[:8]
    sanitized_name = f"{sanitize_text(title)}_{unique_id}.{ext}"
    s3_key = f"{folder}/{sanitized_name}"
    logger.info(f"Generated S3 key before creation: {s3_key}")
    return s3_key


@sync_to_async
def create_or_update_resume(profile, title, file):
    """Create new resume or update existing one"""
    with transaction.atomic():
        try:
            # Try to get existing resume
            resume = Resume.objects.get(user_profile=profile, title=title)
            logger.info(f"Found existing resume with title '{title}', updating...")
            
            # Generate new S3 key
            s3_key = generate_resume_s3_key(profile, title, file)
            
            # Delete old file if it exists
            if resume.file:
                logger.info(f"Deleting old file: {resume.s3_key}")
                resume.file.delete(save=False)
            
            # Update resume
            resume.original_filename = file.name
            resume.s3_key = s3_key
            file.instance = resume
            resume.file = file
            resume.save()
            logger.info(f"Updated resume: {resume.id}")
            
        except Resume.DoesNotExist:
            # Check resume limit before creating new one
            resume_count = Resume.objects.filter(user_profile=profile).count()
            if resume_count >= MAX_RESUMES_PER_USER:
                raise ValidationError(
                    f"Maximum {MAX_RESUMES_PER_USER} resumes allowed. "
                    "Please delete an existing resume first."
                )
            
            # Generate new S3 key
            s3_key = generate_resume_s3_key(profile, title, file)
            
            # Create new resume
            resume = Resume.objects.create(
                user_profile=profile,
                title=title,
                original_filename=file.name,
                s3_key=s3_key
            )
            # Attach resume instance to file and save
            file.instance = resume
            resume.file = file
            resume.save()
            logger.info(f"Created new resume: {resume.id}")
        
        return resume


@sync_to_async
def delete_resume_and_update_default(profile_id: int, resume_id: int):
    """Delete resume and handle default resume logic"""
    with transaction.atomic():
        # Get resume
        resume = get_object_or_404(Resume, id=resume_id, user_profile_id=profile_id)
        was_default = resume.is_default
        
        # Delete the resume
        logger.info(f"Deleting resume: {resume_id}")
        resume.delete()
        
        # If deleted resume was default, update new default
        if was_default:
            logger.info("Deleted resume was default, updating...")
            latest_resume = Resume.objects.filter(
                user_profile_id=profile_id
            ).order_by('-updated_at').first()
            
            if latest_resume:
                latest_resume.is_default = True
                latest_resume.save()
                logger.info(f"Set resume {latest_resume.id} as new default")
        
        return {"success": True}


@sync_to_async
def set_resume_as_default(profile_id: int, resume_id: int):
    """Set a resume as default and ensure others are not default"""
    with transaction.atomic():
        # Get the resume to set as default
        resume = get_object_or_404(Resume, id=resume_id, user_profile_id=profile_id)
        
        # Remove default from all resumes of this profile
        Resume.objects.filter(user_profile_id=profile_id).update(is_default=False)
        
        # Set new default
        resume.is_default = True
        resume.save()
        
        logger.info(f"Set resume {resume_id} as default for profile {profile_id}")
        return resume


@sync_to_async
def get_profile_default_resume(profile_id: int):
    """Get the default resume for a profile"""
    try:
        return Resume.objects.get(user_profile_id=profile_id, is_default=True)
    except Resume.DoesNotExist:
        # If no default exists but resumes exist, set most recent as default
        latest = Resume.objects.filter(user_profile_id=profile_id).order_by('-updated_at').first()
        if latest:
            latest.is_default = True
            latest.save()
            return latest
        return None


