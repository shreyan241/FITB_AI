import os
from typing import Dict
from ninja import Router, File, Form
from ninja.files import UploadedFile
from django.core.exceptions import ValidationError
# from django.shortcuts import get_object_or_404
from django.core.files.storage import Storage
from django.db import transaction
from profiles.models import Resume, UserProfile
from profiles.api.schemas.resume import ResumeCreate, ResumeResponse, MAX_FILE_SIZE, ALLOWED_EXTENSIONS
from profiles.utils.logger.logging_config import logger
from asgiref.sync import sync_to_async


router = Router()

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


@sync_to_async
def create_resume(profile, title, file):
    """Create resume record and save file"""
    with transaction.atomic():
        resume = Resume.objects.create(
            user_profile=profile,
            title=title,
            original_filename=file.name,
            s3_key=''
        )
        
        # Attach resume instance to file for storage class to use
        file.instance = resume
        
        # Save file
        resume.file = file
        resume.save()
        
        return resume

@sync_to_async
def get_or_create_profile():
    """Get or create default profile"""
    profile, _ = UserProfile.objects.get_or_create(id=1)
    return profile

@router.post("/upload", response=ResumeResponse)
async def upload_resume(
    request,
    data: ResumeCreate = Form(...),
    file: UploadedFile = File(...)
):
    """Upload a new resume"""
    logger.info(f"Starting resume upload for file: {file.name}")
    
    try:
        # Validate file
        await validate_resume_file(file)
        
        # Get or create profile
        profile = await get_or_create_profile()
        
        # Create resume and save file
        resume = await create_resume(profile, data.title, file)
            
        logger.info(f"Successfully uploaded resume: {resume.id}")
        return ResumeResponse.from_orm(resume)
        
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise


# @router.post("/upload", response=ResumeResponse)
# async def upload_resume(
#     request,
#     data: ResumeCreate = Form(...),
#     file: UploadedFile = File(...)
# ):
#     """Upload a new resume"""
#     # logger.info(f"Starting resume upload for user: {request.user.username}")
    
#     try:
#         # Validate file
#         await validate_resume_file(file)
#         profile = await UserProfile.objects.aget_or_create(id=1)
        
#         with transaction.atomic():
#             resume = await Resume.objects.acreate(
#                 user_profile= profile,#request.user.profile,
#                 title=data.title,
#                 original_filename=file.name,
#                 s3_key=''
#             )
#             # Attach resume instance to file for storage class to use
#             file.instance = resume
#             # Save file - this triggers ResumeStorage._save()
#             resume.file = file
#             await resume.asave()
#         logger.info(f"Successfully uploaded resume: {resume.id}")
#         return ResumeResponse.from_orm(resume)
#     except ValidationError as e:
#         logger.warning(f"Validation error: {str(e)}")
#         raise
#     except Exception as e:
#         logger.error(f"Upload error: {str(e)}")
        # raise

# @router.delete("/{resume_id}", response=Dict[str, bool])
# async def delete_resume(request, resume_id: int):
#     """Delete a resume and its associated file"""
#     logger.info(f"Delete request for resume {resume_id} from user: {request.user.username}")
    
#     try:
#         # Get resume and verify ownership
#         resume = await get_object_or_404(
#             Resume, 
#             id=resume_id, 
#             user_profile=request.user.profile
#         )
#         logger.debug(f"Found resume: {resume.title} (s3_key: {resume.s3_key})")
        
#         # Delete file from S3 first
#         if resume.s3_key:
#             logger.debug(f"Deleting file from S3: {resume.s3_key}")
#             storage = Storage('RESUMES')
#             storage.delete(resume.s3_key)
#             logger.info(f"Successfully deleted file from S3: {resume.s3_key}")
        
#         # Delete resume record
#         logger.debug(f"Deleting resume record: {resume_id}")
#         await resume.delete()
#         logger.info(f"Successfully deleted resume: {resume_id}")
        
#         return {"success": True}
        
#     except Resume.DoesNotExist:
#         logger.warning(f"Resume not found: {resume_id}")
#         raise
#     except Exception as e:
#         logger.error(f"Error deleting resume {resume_id}: {str(e)}")
#         raise