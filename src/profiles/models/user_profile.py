from django.db import models, transaction
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Personal Details
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
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

    @property
    def default_resume(self):
        """Returns the user's default resume or None if no resume exists."""
        return self.resumes.filter(is_default=True).first()

    def set_default_resume(self, resume_id):
        """Sets the specified resume as default and unsets any existing default."""
        if not self.resumes.filter(id=resume_id).exists():
            raise ValueError("Resume does not exist or doesn't belong to this user")
        
        with transaction.atomic():
            # Unset current default
            self.resumes.filter(is_default=True).update(is_default=False)
            # Set new default
            self.resumes.filter(id=resume_id).update(is_default=True)
            
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username
    