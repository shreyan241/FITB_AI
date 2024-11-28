from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Education(models.Model):
    DEGREE_CHOICES = [
        ("High School", "High School"),
        ("Associate's", "Associate's"),
        ("Bachelor's", "Bachelor's"),
        ("Master's", "Master's"),
        ("PhD", "PhD"),
        ("MBA", "MBA"),
        ("MD", "MD"),
        ("JD", "JD"),
        ("Bootcamp", "Bootcamp"),
        ("Certification", "Certification"),
        ("Other", "Other")
    ]
    
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='education')
    school_name = models.CharField(max_length=255)
    degree_type = models.CharField(max_length=50, choices=DEGREE_CHOICES)
    major = models.CharField(max_length=255, blank=True)
    minor = models.CharField(max_length=255, blank=True)
    
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
    
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(4)]
    )

    class Meta:
        ordering = ['-start_year', '-start_month']
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree_type} in {self.major} at {self.school_name}"