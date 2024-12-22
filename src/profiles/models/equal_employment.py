from django.db import models
from profiles.models import UserProfile

class EqualEmploymentData(models.Model):
    ETHNICITY_CHOICES = [
        ('Hispanic or Latino', 'Hispanic or Latino'),
        ('White (Not Hispanic or Latino)', 'White (Not Hispanic or Latino)'),
        ('Black or African American (Not Hispanic or Latino)', 'Black or African American (Not Hispanic or Latino)'),
        ('Native American or Alaska Native (Not Hispanic or Latino)', 'Native American or Alaska Native (Not Hispanic or Latino)'),
        ('Asian (Not Hispanic or Latino)', 'Asian (Not Hispanic or Latino)'),
        ('Native Hawaiian or Other Pacific Islander (Not Hispanic or Latino)', 
         'Native Hawaiian or Other Pacific Islander (Not Hispanic or Latino)'),
        ('Two or More Races (Not Hispanic or Latino)', 'Two or More Races (Not Hispanic or Latino)'),
        ('Decline to self-identify', 'Decline to self-identify')
    ]
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-Binary', 'Non-Binary'),
        ('Transgender', 'Transgender'),
        ('Other', 'Other'),
        ('Decline to self-identify', 'Decline to self-identify')
    ]
    
    VETERAN_STATUS_CHOICES = [
        ('I am not a protected veteran', 'I am not a protected veteran'),
        ('I identify as one or more of the classifications of protected veteran', 
         'I identify as one or more of the classifications of protected veteran'),
        ('Decline to self-identify', 'Decline to self-identify')
    ]
    
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='equal_employment_data')
    
    # Demographics
    ethnicity = models.CharField(max_length=100, choices=ETHNICITY_CHOICES)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    
    # Employment Eligibility
    is_authorized_to_work = models.BooleanField(
        verbose_name="Are you legally authorized to work in the United States?"
    )
    will_require_sponsorship = models.BooleanField(
        verbose_name="Will you now or in the future require sponsorship for employment visa status?"
    )
    
    # Protected Status
    has_disability = models.BooleanField(
        verbose_name="Do you have a disability as defined by the Americans with Disabilities Act?",
        null=True,
        blank=True
    )
    veteran_status = models.CharField(
        max_length=100,
        choices=VETERAN_STATUS_CHOICES,
        verbose_name="Protected Veteran Status"
    )
    
    class Meta:
        verbose_name = "Equal Employment Data"
        verbose_name_plural = "Equal Employment Data"

    def __str__(self):
        return f"EEO Data for {self.user_profile.first_name} {self.user_profile.last_name}"