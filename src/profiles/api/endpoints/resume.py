from ninja import Router, File, Form
from ninja.files import UploadedFile
from django.core.exceptions import ValidationError
# from django.shortcuts import get_object_or_404
from profiles.api.helpers.resume import validate_resume_file, create_or_update_resume
from profiles.models import UserProfile
from profiles.api.schemas.resume import ResumeCreate, ResumeResponse
from profiles.utils.logger.logging_config import logger
from asgiref.sync import sync_to_async


router = Router()

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
    """Upload or update a new resume"""
    logger.info(f"Starting resume upload for file: {file.name}")
    
    try:
        # Validate file
        await validate_resume_file(file)
        
        # Get or create profile
        profile = await get_or_create_profile()
        
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