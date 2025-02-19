from django.db import models
from profiles.models.custom_user import CustomUser
from django.core.validators import EmailValidator

class UserProfile(models.Model):
    # Link to Django User
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    # Personal Details
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    application_email = models.EmailField(
        max_length=255, 
        blank=True,
        validators=[EmailValidator()],
        help_text="Email to use for job applications. If blank, account email will be used."
    )
    phone_number = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Location
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Skills
    skills = models.ManyToManyField('Skill', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.email
    
    @property
    def full_name(self):
        """Return user's full name from profile, fallback to user's name"""
        profile_name = f"{self.first_name} {self.last_name}".strip()
        if profile_name:
            return profile_name
        user_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return user_name or self.user.email
    
    @property
    def email(self):
        """Return application email if set, otherwise return account email"""
        return self.application_email or self.user.email
    