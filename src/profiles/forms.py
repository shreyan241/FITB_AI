from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from profiles.models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 
            'last_name',
            'phone_number', 
            'birth_date', 
            'city', 
            'state', 
            'country'
        ]