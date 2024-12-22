from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from profiles.utils.storage.resume_storage import ResumeStorage
from profiles.models import UserProfile
from profiles.utils.logger.logging_config import logger

# Constants
MAX_TITLE_LENGTH = 100
MAX_FILENAME_LENGTH = 255
MAX_RESUMES_PER_USER = 3

class Resume(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='resumes'
    )
    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        help_text=_("A unique title for this resume")
    )
    original_filename = models.CharField(max_length=MAX_FILENAME_LENGTH)
    s3_key = models.CharField(max_length=MAX_FILENAME_LENGTH, unique=True)
    file = models.FileField(
        storage=ResumeStorage(),
        upload_to='',  # Path handled by storage class
        blank=True,
        null=True
    )
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        constraints = [
            # Ensure title is unique per user
            models.UniqueConstraint(
                fields=['user_profile', 'title'],
                name='unique_resume_title_per_user'
            ),
            # Ensure only one default resume per user
            models.UniqueConstraint(
                fields=['user_profile'],
                condition=models.Q(is_default=True),
                name='unique_default_resume'
            )
        ]

    def clean(self):
        """Validate resume count"""
        if not self.pk:  # Only check on creation
            # Check resume count
            resume_count = Resume.objects.filter(user_profile=self.user_profile).count()
            if resume_count >= MAX_RESUMES_PER_USER:
                raise ValidationError(
                    _(f"Maximum of {MAX_RESUMES_PER_USER} resumes allowed. Please delete an existing resume first.")
                )

    def save(self, *args, **kwargs):
        """Save resume and handle default status"""
        self.full_clean()
        
        # Make first resume default
        if not self.pk and not Resume.objects.filter(user_profile=self.user_profile).exists():
            self.is_default = True
            
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete resume and its S3 file"""
        try:
            # Store if this was the default resume
            was_default = self.is_default
            
            # Delete the file
            if self.file:
                logger.info(f"Deleting S3 file for resume: {self.s3_key}")
                self.file.delete(save=False)
            
            # Delete the database record
            super().delete(*args, **kwargs)
            logger.info(f"Deleted resume record: {self.id}")
            
            # If this was the default resume, set a new one
            if was_default:
                logger.info("Deleted resume was default, updating...")
                latest_resume = Resume.objects.filter(
                    user_profile=self.user_profile
                ).order_by('-updated_at').first()
                
                if latest_resume:
                    latest_resume.is_default = True
                    latest_resume.save()
                    logger.info(f"Set resume {latest_resume.id} as new default")
                else:
                    logger.info("No resumes left to set as default")
        except Exception as e:
            logger.error(f"Error deleting S3 file: {str(e)}")
            raise

    def __str__(self):
        return f"{self.title} ({self.user_profile.user.username})"