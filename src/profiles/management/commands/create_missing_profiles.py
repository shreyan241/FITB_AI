from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import UserProfile
from profiles.utils.logger.logging_config import logger

class Command(BaseCommand):
    help = 'Create UserProfile for users that do not have one'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(userprofile__isnull=True)
        count = users_without_profiles.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('All users have profiles!'))
            return
            
        self.stdout.write(f'Found {count} users without profiles')
        
        for user in users_without_profiles:
            try:
                UserProfile.objects.create(user=user)
                logger.info(f"Created profile for user {user.id}")
                self.stdout.write(self.style.SUCCESS(f'Created profile for {user.username}'))
            except Exception as e:
                logger.error(f"Error creating profile for user {user.id}: {str(e)}")
                self.stdout.write(
                    self.style.ERROR(f'Failed to create profile for {user.username}: {str(e)}')
                ) 