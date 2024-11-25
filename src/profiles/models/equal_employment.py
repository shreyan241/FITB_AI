from django.db import models
from profiles.models import UserProfile

class EqualEmployment(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    gender = models.CharField(max_length=30, blank=True)
    ethnicity = models.CharField(max_length=50, blank=True)
    veteran_status = models.BooleanField(default=False)
    # Add other equal employment fields 