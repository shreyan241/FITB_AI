from django import forms
from django.contrib.auth.forms import UserCreationForm
from profiles.models import UserProfile, CustomUser

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'application_email',
            'phone_number', 
            'birth_date', 
            'city', 
            'state', 
            'country'
        ]