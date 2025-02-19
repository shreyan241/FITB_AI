from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from profiles.models import UserProfile, CustomUser
from django.apps import apps
from profiles.utils.logger.logging_config import logger

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile when user is created/updated"""
    try:
        # Get or create the profile
        profile, was_created = UserProfile.objects.get_or_create(user=instance)
        if was_created:
            logger.info(f"Created new profile for user {instance.id}")
        else:
            profile.save()
            logger.info(f"Updated profile for user {instance.id}")
    except Exception as e:
        logger.error(f"Error in create_or_update_user_profile signal: {str(e)}")

@receiver(post_migrate)
def create_missing_profiles(sender, **kwargs):
    """Create missing profiles after migrations"""
    if sender.name == 'profiles':  # Only run for profiles app
        try:
            User = apps.get_model('profiles', 'CustomUser')
            UserProfile = apps.get_model('profiles', 'UserProfile')
            
            # Get users without profiles
            users_without_profiles = User.objects.filter(userprofile__isnull=True)
            
            # Create profiles for users without them
            for user in users_without_profiles:
                UserProfile.objects.create(user=user)
                logger.info(f"Created missing profile for user {user.id}")
                
        except Exception as e:
            logger.error(f"Error in create_missing_profiles signal: {str(e)}")
