# Generated by Django 5.1.3 on 2024-11-30 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resume",
            name="s3_key",
        ),
        migrations.AlterField(
            model_name="resume",
            name="is_default",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="resume",
            name="title",
            field=models.CharField(
                help_text="A unique title for this resume", max_length=100
            ),
        ),
        migrations.AddConstraint(
            model_name="resume",
            constraint=models.UniqueConstraint(
                fields=("user_profile", "title"), name="unique_resume_title_per_user"
            ),
        ),
    ]
