from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from profiles.utils.storage.resume_storage import ResumeStorage


# Common constants
MAX_TITLE_LENGTH = 100
MAX_FILENAME_LENGTH = 255
MAX_RESUMES_PER_USER = 3

# Initialize storage
resume_storage = ResumeStorage()

class Resume(models.Model):
    user_profile = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
        related_name='resumes'
    )
    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        help_text=_("E.g., 'Data Scientist Resume', 'Software Engineer Resume'")
    )
    original_filename = models.CharField(max_length=MAX_FILENAME_LENGTH)
    s3_key = models.CharField(max_length=MAX_FILENAME_LENGTH, unique=True, blank=True, null=True)
    file = models.FileField(
        storage=resume_storage,
        upload_to='',  # Path will be handled by ResumeStorage
        null=True,
        blank=True
    )
    is_default = models.BooleanField(
        default=False,
        help_text=_("Use this resume as the default for job applications")
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user_profile'],
                condition=models.Q(is_default=True),
                name='unique_default_resume'
            )
        ]

    def clean(self):
        if not self.pk:  # Only check on creation
            resume_count = Resume.objects.filter(user_profile=self.user_profile).count()
            if resume_count >= MAX_RESUMES_PER_USER:
                raise ValidationError(_(f"Maximum of {MAX_RESUMES_PER_USER} resumes allowed per user."))

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk and not Resume.objects.filter(user_profile=self.user_profile).exists():
            self.is_default = True
        super().save(*args, **kwargs)

    def __str__(self):
        default_str = " (Default)" if self.is_default else ""
        return f"{self.title}{default_str} - {self.user_profile.user.username}"