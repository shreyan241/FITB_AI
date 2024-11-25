from django.db import models
from django.contrib.auth.models import User
from profiles.utils.validators import FileValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Contact Details
    phone_number = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    # Resume upload
    resume = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True,
        # Add validators for file type and size
        validators=[FileValidator(
            max_size=1024 * 1024 * 5,  # 5MB max
            content_types=('application/pdf', 'application/msword', 'text/plain', 
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        )]
    )
    # Skills
    skills = models.ManyToManyField('Skill', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username