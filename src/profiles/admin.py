from django.contrib import admin
from profiles.models import (
    UserProfile,
    Education,
    WorkExperience,
    EqualEmployment,
    SocialLink,
    Skill
)

# Register your models
admin.site.register(UserProfile)
admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(EqualEmployment)
admin.site.register(SocialLink)
admin.site.register(Skill)
