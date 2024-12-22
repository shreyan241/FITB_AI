# Generated by Django 5.1.3 on 2024-12-22 00:58

import django.core.validators
import django.db.models.deletion
import profiles.utils.storage.resume_storage
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Skill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=100)),
                ("last_name", models.CharField(blank=True, max_length=100)),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=255,
                        validators=[django.core.validators.EmailValidator()],
                    ),
                ),
                ("phone_number", models.CharField(blank=True, max_length=20)),
                ("birth_date", models.DateField(blank=True, null=True)),
                ("city", models.CharField(blank=True, max_length=100)),
                ("state", models.CharField(blank=True, max_length=100)),
                ("country", models.CharField(blank=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("skills", models.ManyToManyField(blank=True, to="profiles.skill")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="EqualEmploymentData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ethnicity",
                    models.CharField(
                        choices=[
                            ("Hispanic or Latino", "Hispanic or Latino"),
                            (
                                "White (Not Hispanic or Latino)",
                                "White (Not Hispanic or Latino)",
                            ),
                            (
                                "Black or African American (Not Hispanic or Latino)",
                                "Black or African American (Not Hispanic or Latino)",
                            ),
                            (
                                "Native American or Alaska Native (Not Hispanic or Latino)",
                                "Native American or Alaska Native (Not Hispanic or Latino)",
                            ),
                            (
                                "Asian (Not Hispanic or Latino)",
                                "Asian (Not Hispanic or Latino)",
                            ),
                            (
                                "Native Hawaiian or Other Pacific Islander (Not Hispanic or Latino)",
                                "Native Hawaiian or Other Pacific Islander (Not Hispanic or Latino)",
                            ),
                            (
                                "Two or More Races (Not Hispanic or Latino)",
                                "Two or More Races (Not Hispanic or Latino)",
                            ),
                            ("Decline to self-identify", "Decline to self-identify"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Non-Binary", "Non-Binary"),
                            ("Transgender", "Transgender"),
                            ("Other", "Other"),
                            ("Decline to self-identify", "Decline to self-identify"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "is_authorized_to_work",
                    models.BooleanField(
                        verbose_name="Are you legally authorized to work in the United States?"
                    ),
                ),
                (
                    "will_require_sponsorship",
                    models.BooleanField(
                        verbose_name="Will you now or in the future require sponsorship for employment visa status?"
                    ),
                ),
                (
                    "has_disability",
                    models.BooleanField(
                        blank=True,
                        null=True,
                        verbose_name="Do you have a disability as defined by the Americans with Disabilities Act?",
                    ),
                ),
                (
                    "veteran_status",
                    models.CharField(
                        choices=[
                            (
                                "I am not a protected veteran",
                                "I am not a protected veteran",
                            ),
                            (
                                "I identify as one or more of the classifications of protected veteran",
                                "I identify as one or more of the classifications of protected veteran",
                            ),
                            ("Decline to self-identify", "Decline to self-identify"),
                        ],
                        max_length=100,
                        verbose_name="Protected Veteran Status",
                    ),
                ),
                (
                    "user_profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="equal_employment_data",
                        to="profiles.userprofile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Equal Employment Data",
                "verbose_name_plural": "Equal Employment Data",
            },
        ),
        migrations.CreateModel(
            name="Education",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("school_name", models.CharField(max_length=255)),
                (
                    "degree_type",
                    models.CharField(
                        choices=[
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
                            ("Other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("major", models.CharField(blank=True, max_length=255)),
                ("minor", models.CharField(blank=True, max_length=255)),
                (
                    "start_month",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ]
                    ),
                ),
                ("start_year", models.IntegerField()),
                (
                    "end_month",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ],
                    ),
                ),
                ("end_year", models.IntegerField(blank=True, null=True)),
                ("is_current", models.BooleanField(default=False)),
                (
                    "gpa",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=3,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(4),
                        ],
                    ),
                ),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="education",
                        to="profiles.userprofile",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Education",
                "ordering": ["-start_year", "-start_month"],
            },
        ),
        migrations.CreateModel(
            name="WorkExperience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company", models.CharField(max_length=255)),
                ("position_title", models.CharField(max_length=255)),
                (
                    "employment_type",
                    models.CharField(
                        choices=[
                            ("Full-time", "Full-time"),
                            ("Part-time", "Part-time"),
                            ("Contract", "Contract"),
                            ("Temporary", "Temporary"),
                            ("Internship", "Internship"),
                            ("Apprenticeship", "Apprenticeship"),
                            ("Freelance", "Freelance"),
                            ("Volunteer", "Volunteer"),
                            ("Other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                ("is_remote", models.BooleanField(default=False)),
                (
                    "start_month",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ]
                    ),
                ),
                ("start_year", models.IntegerField()),
                (
                    "end_month",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ],
                    ),
                ),
                ("end_year", models.IntegerField(blank=True, null=True)),
                ("is_current", models.BooleanField(default=False)),
                ("description", models.TextField()),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="work_experiences",
                        to="profiles.userprofile",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Work Experience",
                "ordering": ["-start_year", "-start_month"],
            },
        ),
        migrations.CreateModel(
            name="SocialLink",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "platform",
                    models.CharField(
                        choices=[
                            ("LinkedIn", "LinkedIn"),
                            ("GitHub", "GitHub"),
                            ("Twitter", "Twitter"),
                            ("Portfolio", "Portfolio"),
                            ("Other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "url",
                    models.URLField(validators=[django.core.validators.URLValidator()]),
                ),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="social_links",
                        to="profiles.userprofile",
                    ),
                ),
            ],
            options={
                "unique_together": {("user_profile", "platform")},
            },
        ),
        migrations.CreateModel(
            name="Resume",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="A unique title for this resume", max_length=100
                    ),
                ),
                ("original_filename", models.CharField(max_length=255)),
                ("s3_key", models.CharField(max_length=255, unique=True)),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        storage=profiles.utils.storage.resume_storage.ResumeStorage(),
                        upload_to="",
                    ),
                ),
                ("is_default", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resumes",
                        to="profiles.userprofile",
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("user_profile", "title"),
                        name="unique_resume_title_per_user",
                    ),
                    models.UniqueConstraint(
                        condition=models.Q(("is_default", True)),
                        fields=("user_profile",),
                        name="unique_default_resume",
                    ),
                ],
            },
        ),
    ]
