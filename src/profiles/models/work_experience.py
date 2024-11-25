from django.db import models
from django.forms import ValidationError
from profiles.models import UserProfile

class WorkExperience(models.Model):
    EXPERIENCE_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
        ('Freelance', 'Freelance'),
        ('Volunteer', 'Volunteer')
    ]
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='work_experiences')
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    position_title = models.CharField(max_length=255)
    experience_type = models.CharField(max_length=50, choices=EXPERIENCE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    description = models.TextField()

    class Meta:
        ordering = ['-start_date']

    def clean(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date")
        if self.currently_working and self.end_date:
            raise ValidationError("Current position cannot have an end date")
    
    def __str__(self):
        return f"{self.position_title} at {self.company}"