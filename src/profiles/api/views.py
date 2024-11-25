from django.shortcuts import render, redirect
from profiles.forms import UserRegistrationForm, UserProfileForm
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profiles.models import UserProfile
from profiles.api.serializers import UserProfileSerializer, ResumeUploadSerializer
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


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=True, methods=['POST'], url_path='upload-resume')
    def upload_resume(self, request, pk=None):
        try:
            profile = self.get_object()
            
            if 'resume' not in request.FILES:
                return Response(
                    {'error': 'No resume file provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = ResumeUploadSerializer(
                profile,
                data={'resume': request.FILES['resume']},
                partial=True
            )

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Delete old resume if exists
            profile.delete_resume()
            
            # Save new resume
            profile = serializer.save()
            
            logger.info(f"Resume uploaded for user {profile.user.username}: {profile.resume.name}")

            return Response({
                'message': 'Resume uploaded successfully',
                'resume_url': profile.get_resume_url()
            })

        except Exception as e:
            logger.error(f"Error uploading resume: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )