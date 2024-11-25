from django.db import models
from django.core.validators import URLValidator
from profiles.models import UserProfile

class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('LinkedIn', 'LinkedIn'),
        ('GitHub', 'GitHub'),
        ('Twitter', 'Twitter'),
        ('Portfolio', 'Portfolio'),
        ('Other', 'Other')
    ]
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField(validators=[URLValidator()])

    class Meta:
        unique_together = ['user_profile', 'platform']
    
    def __str__(self):
        return f"{self.platform} profile"

