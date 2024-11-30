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


def check_profile_access(request, profile_id: int):
    """
    Check if user has access to profile
    Raises PermissionError if access denied
    """
    if not request.user.is_authenticated:
        raise PermissionError("Authentication required")
        
    if request.user.profile.id != profile_id:
        logger.warning(f"Unauthorized access attempt to profile {profile_id} by user {request.user.id}")
        raise PermissionError("You don't have permission to access this profile")


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


def get_existing_resume(profile, title):
    """Get existing resume by title"""
    try:
        return Resume.objects.get(user_profile=profile, title=title)
    except Resume.DoesNotExist:
        return None


def check_resume_limit(profile):
    """Check if user has reached resume limit"""
    count = Resume.objects.filter(user_profile=profile).count()
    if count >= MAX_RESUMES_PER_USER:
        raise ValidationError(
            f"Maximum {MAX_RESUMES_PER_USER} resumes allowed. "
            "Please delete an existing resume first."
        )


@sync_to_async
def create_or_update_resume(profile, title, file):
    """Create new resume or update existing one"""
    with transaction.atomic():
        # Get existing resumes
        existing_resume = get_existing_resume(profile, title)
        # If no existing resume, check limit
        if not existing_resume:
            check_resume_limit(profile)
        # Generate new S3 key
        s3_key = generate_resume_s3_key(profile, title, file)
        # Delete existing resume if updating
        if existing_resume:
            logger.info(f"Updating existing resume: {existing_resume.id}")
            existing_resume.delete()
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
        logger.info(f"{'Updated' if existing_resume else 'Created'} resume: {resume.id}")
        return resume
    

def update_default_resume(profile):
    """Update default resume after deletion"""
    # Get most recently updated resume
    latest_resume = Resume.objects.filter(
        user_profile=profile
    ).order_by('-updated_at').first()
    if latest_resume:
        logger.info(f"Setting resume {latest_resume.id} as default for profile {profile.id}")
        latest_resume.is_default = True
        latest_resume.save()
        return latest_resume
    logger.info(f"No resumes left for profile {profile.id}")
    return None


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
            profile = get_object_or_404(UserProfile, id=profile_id)
            update_default_resume(profile)
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


