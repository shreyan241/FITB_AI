import os 
import uuid
from threading import local
from django.utils.text import slugify
from storages.backends.s3boto3 import S3Boto3Storage

class ResumeStorage(S3Boto3Storage):
    location = 'resumes'  # folder in bucket
    file_overwrite = False
    default_acl = 'private'  # Ensure files are private
    querystring_auth = True  # Add authentication to URLs
    custom_domain = None  # Use S3 domain, not custom domain

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread_local = local()
    
    def get_unique_filename(self, filename, instance):
        """
        Generate a unique filename while preserving the original extension.
        Format: username_uuid8_sanitized_filename.ext
        """
        # Get the filename and extension
        name, ext = os.path.splitext(filename)
        
        # Sanitize the original filename
        sanitized_name = slugify(name)
        
        # Generate unique filename with username and uuid
        unique_name = f"{instance.user.username}_{uuid.uuid4().hex[:8]}_{sanitized_name}{ext}"
        
        # Return the full path including the location (resumes folder)
        return os.path.join(self.location, unique_name)

    def get_available_name(self, name, max_length=None):
        """
        Override get_available_name to use our naming scheme
        """
        try:
            if hasattr(self.thread_local, 'current_instance'):
                instance = self.thread_local.current_instance
                name = self.get_unique_filename(name, instance)
        except AttributeError:
            # If no instance is available, just use a UUID
            name, ext = os.path.splitext(name)
            name = f"{uuid.uuid4().hex[:8]}_{name}{ext}"
            name = os.path.join(self.location, name)
        
        return super().get_available_name(name, max_length)
    
    def _save(self, name, content):
        """
        Override _save to handle the instance context
        """
        try:
            if hasattr(content, 'instance'):
                self.thread_local.current_instance = content.instance
                try:
                    return super()._save(name, content)
                finally:
                    delattr(self.thread_local, 'current_instance')
        except AttributeError:
            pass
        
        return super()._save(name, content)