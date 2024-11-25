from rest_framework import serializers
from profiles.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'phone_number', 'birth_date', 'city', 
                 'state', 'country', 'resume', 'resume_url']
        read_only_fields = ['resume_url']

    def get_resume_url(self, obj):
        return obj.get_resume_url()

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['resume']