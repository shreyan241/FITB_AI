from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from profiles.models import UserProfile
class WorkExperience(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Temporary', 'Temporary'),
        ('Internship', 'Internship'),
        ('Apprenticeship', 'Apprenticeship'),
        ('Freelance', 'Freelance'),
        ('Volunteer', 'Volunteer'),
        ('Other', 'Other')
    ]
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='work_experiences')
    company = models.CharField(max_length=255)
    position_title = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES)
    
    # Location
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_remote = models.BooleanField(default=False)
    
    # Month-Year format fields
    start_month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    start_year = models.IntegerField()
    end_month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        null=True,
        blank=True
    )
    end_year = models.IntegerField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    description = models.TextField()
    
    class Meta:
        ordering = ['-start_year', '-start_month']
        verbose_name_plural = "Work Experience"

    def __str__(self):
        return f"{self.position_title} at {self.company}"