from django.contrib import admin
from .models import UserProfile, Education, WorkExperience, SocialLink, Skill, EqualEmploymentData

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(SocialLink)
admin.site.register(Skill)
admin.site.register(EqualEmploymentData)
