from django.db import models
from django.forms import ValidationError
from profiles.models import UserProfile

class Education(models.Model):
    DEGREE_CHOICES = [
        ("Bachelor's", "Bachelor's"),
        ("Master's", "Master's"),
        ("PhD", "PhD"),
        ("MBA", "MBA"),
        ("Associate's", "Associate's"),
        ("MD", "MD"),
        ("JD", "JD"),
        ("Bootcamp", "Bootcamp"),
        ("Certification", "Certification")
    ]
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='education')
    school_name = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    degree_type = models.CharField(max_length=50, choices=DEGREE_CHOICES)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def clean(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date")
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.degree_type} in {self.major} at {self.school_name}"
