from django.db import models
from django.contrib.postgres.fields import ArrayField
from profiles.models import UserProfile

class EqualEmploymentData(models.Model):
    ETHNICITY_CHOICES = [
        ('Black/African American', 'Black/African American'),
        ('East Asian', 'East Asian'),
        ('South Asian', 'South Asian'),
        ('Hispanic/Latinx', 'Hispanic/Latinx'),
        ('Southeast Asian', 'Southeast Asian'),
        ('Middle Eastern', 'Middle Eastern'),
        ('African', 'African'),
        ('Native American/Alaskan', 'Native American/Alaskan'),
        ('Native Hawaiian/Other Pacific Islander', 'Native Hawaiian/Other Pacific Islander'),
        ('White', 'White'),
    ]
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-Binary', 'Non-Binary'),
        ('Decline to state', 'Decline to state')
    ]
    
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    
    YES_NO_DECLINE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Decline to state', 'Decline to state')
    ]
    
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='equal_employment_data')
    
    # Work Authorization
    authorized_us = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Are you authorized to work in the US?",
        blank=True,
        null=True
    )
    authorized_canada = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Are you authorized to work in Canada?",
        blank=True,
        null=True
    )
    authorized_uk = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Are you authorized to work in the United Kingdom?",
        blank=True,
        null=True
    )
    requires_sponsorship = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Will you now or in the future require sponsorship for employment visa status?",
        blank=True,
        null=True
    )
    
    # Demographics
    ethnicities = ArrayField(
        models.CharField(max_length=100, choices=ETHNICITY_CHOICES),
        blank=True,
        default=list,
        verbose_name="What is your ethnicity? (Select all that apply)"
    )
    is_hispanic_latinx = models.BooleanField(
        default=False,
        editable=False,  # This field is auto-populated
        verbose_name="Hispanic/Latinx"
    )
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        verbose_name="What is your gender?",
        blank=True,
        null=True
    )
    
    # Additional Information
    has_disability = models.CharField(
        max_length=20,
        choices=YES_NO_DECLINE_CHOICES,
        verbose_name="Do you have a disability?",
        blank=True,
        null=True
    )
    is_lgbtq = models.CharField(
        max_length=20,
        choices=YES_NO_DECLINE_CHOICES,
        verbose_name="Do you identify as LGBTQ+?",
        blank=True,
        null=True
    )
    is_veteran = models.CharField(
        max_length=20,
        choices=YES_NO_DECLINE_CHOICES,
        verbose_name="Are you a veteran?",
        blank=True,
        null=True
    )
    
    def save(self, *args, **kwargs):
        # Auto-populate is_hispanic_latinx based on ethnicities
        self.is_hispanic_latinx = 'Hispanic/Latinx' in self.ethnicities
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Equal Employment Data"
        verbose_name_plural = "Equal Employment Data"

    def __str__(self):
        return f"EEO Data for {self.user_profile.first_name} {self.user_profile.last_name}"