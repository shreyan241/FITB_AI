from django.contrib import admin
from profiles.models import (
    UserProfile,
    Education,
    WorkExperience,
    EqualEmploymentData,
    SocialLink,
    Skill,
    Resume,
)   

# Register your models
admin.site.register(UserProfile)
admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(EqualEmploymentData)
admin.site.register(SocialLink)
admin.site.register(Skill)
admin.site.register(Resume)
