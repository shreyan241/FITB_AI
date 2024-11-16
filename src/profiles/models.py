from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .validators import FileValidator


# Create your models here.

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

class Skill(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
class EqualEmploymentData(models.Model):
    ETHNICITY_CHOICES = [
        ('Hispanic or Latino', 'Hispanic or Latino'),
        ('White', 'White'),
        ('Black or African American', 'Black or African American'),
        ('Native American or American Indian', 'Native American or American Indian'),
        ('Asian / Pacific Islander', 'Asian / Pacific Islander'),
        ('Other', 'Other'),
        ('Decline to state', 'Decline to state'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-Binary', 'Non-Binary'),
        ('Decline to state', 'Decline to state'),
    ]
    YES_NO_DECLINE = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Decline to state', 'Decline to state'),
    ]
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='equal_employment_data')
    ethnicity = models.CharField(max_length=50, choices=ETHNICITY_CHOICES)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    authorized_us = models.BooleanField(verbose_name="Authorized to work in US")
    requires_sponsorship = models.BooleanField(verbose_name="Requires visa sponsorship")
    disability = models.CharField(
        max_length=20,
        choices=YES_NO_DECLINE,
        verbose_name="Do you have a disability?"
    )
    veteran_status = models.CharField(
        max_length=20,
        choices=YES_NO_DECLINE,
        verbose_name="Are you a protected veteran?"
    )
    lgbtq = models.CharField(
        max_length=20,
        choices=YES_NO_DECLINE,
        verbose_name="Do you identify as LGBTQ+?"
    )

    class Meta:
        verbose_name = "Equal Employment Data"
        verbose_name_plural = "Equal Employment Data"

    def __str__(self):
        return f"Equal Employment Data for {self.user_profile.user.username}"
