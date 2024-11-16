from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib import messages
from backend.logging_config import logger

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Your account has been created.')
            logger.info(f"New user registered: {user.username}")
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'profiles/register.html', context)
