from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from uuid import uuid4
from profiles.utils.validators.text import sanitize_text
from profiles.utils.logger.logging_config import logger

class ResumeStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'resumes'
    
    def _save(self, name, content):
        """Called when resume.file = file is executed"""
        logger.info(f"Starting file save process for file: {name}")
        
        # Get resume instance from content
        instance = getattr(content, 'instance', None)
        logger.debug(f"Retrieved instance: {instance and instance.id}")
        
        if instance:
            # Generate S3 filename
            filename = self.generate_filename(name)
            logger.info(f"Generated S3 filename: {filename}")
            
            # Delete old file if updating
            if instance.pk and instance.s3_key:
                logger.info(f"Deleting old file: {instance.s3_key}")
                self.delete(instance.s3_key)
            
            # Upload to S3
            logger.debug(f"Uploading file to S3, size: {content.size} bytes")
            name = super()._save(filename, content)
            logger.info(f"File uploaded successfully to: {name}")
            
            # Update resume record
            instance.s3_key = name
            instance.save(update_fields=['s3_key'])
            logger.info(f"Updated resume record {instance.id} with s3_key: {name}")
            
        return name

    def generate_filename(self, filename):
        """Generate a unique filename for S3"""
        # Extract extension
        ext = filename.split('.')[-1].lower() if '.' in filename else ''
        
        # Generate unique ID
        unique_id = str(uuid4())[:8]
        
        # Create sanitized filename
        base_name = sanitize_text(filename.rsplit('.', 1)[0])
        new_name = f"{base_name}_{unique_id}.{ext}"
        
        # Create full path including location
        full_path = f"{self.location}/{new_name}"
        
        logger.debug(f"Generated filename: {full_path}")
        return full_path

    def delete(self, name):
        """Delete the specified file from storage."""
        logger.info(f"Deleting file from S3: {name}")
        try:
            self.bucket.Object(name).delete()
            logger.info(f"Successfully deleted file: {name}")
        except Exception as e:
            logger.error(f"Error deleting file {name}: {str(e)}")
            raise