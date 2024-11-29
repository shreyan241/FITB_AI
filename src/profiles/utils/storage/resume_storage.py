from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from profiles.utils.logger.logging_config import logger

class ResumeStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    def _save(self, name, content):
        """Called when resume.file = file is executed"""
        logger.info(f"Starting file save process for file: {name}")
        
        instance = getattr(content, 'instance', None)
        logger.debug(f"Retrieved instance: {instance and instance.id}")
        
        if instance:
            try:
                # Use the existing s3_key from the instance
                s3_key = instance.s3_key
                logger.info(f"Using pre-generated S3 key: {s3_key}")
                
                # Delete old file if updating
                if instance.pk and instance.s3_key:
                    logger.info(f"Deleting old file: {instance.s3_key}")
                    self.delete(instance.s3_key)
                
                # Upload to S3 using parent class
                logger.debug(f"Uploading file to S3, size: {content.size} bytes")
                uploaded_s3_key = super()._save(s3_key, content)
                logger.info(f"File uploaded successfully to: {uploaded_s3_key}")
                return uploaded_s3_key
                
            except Exception as e:
                logger.error(f"S3 Upload Error: {str(e)}")
                raise
    
        return name
            
    def delete(self, name):
        """Delete the specified file from storage."""
        logger.info(f"Deleting file from S3: {name}")
        try:
            self.bucket.Object(name).delete()
            logger.info(f"Successfully deleted file: {name}")
        except Exception as e:
            logger.error(f"Error deleting file {name}: {str(e)}")
            raise