from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from profiles.models import SocialLink, UserProfile
from profiles.utils.logger.logging_config import logger

async def create_social_link(profile: UserProfile, platform: str, url: str) -> SocialLink:
    """Create a new social link for a profile"""
    try:
        # Check if platform already exists for this profile
        exists = await sync_to_async(
            lambda: SocialLink.objects.filter(
                user_profile=profile,
                platform=platform
            ).exists()
        )()
        
        if exists:
            raise ValidationError(f"A {platform} link already exists for this profile")
        
        # Create new social link
        social_link = await sync_to_async(SocialLink.objects.create)(
            user_profile=profile,
            platform=platform,
            url=url
        )
        
        return social_link
    except Exception as e:
        logger.error(f"Error creating social link: {str(e)}")
        raise

async def update_social_link(link_id: int, platform: str = None, url: str = None) -> SocialLink:
    """Update an existing social link"""
    try:
        social_link = await sync_to_async(get_object_or_404)(SocialLink, id=link_id)
        
        if platform is not None:
            # Check if new platform already exists for this profile
            if platform != social_link.platform:
                exists = await sync_to_async(
                    lambda: SocialLink.objects.filter(
                        user_profile=social_link.user_profile,
                        platform=platform
                    ).exists()
                )()
                
                if exists:
                    raise ValidationError(f"A {platform} link already exists for this profile")
            
            social_link.platform = platform
        
        if url is not None:
            social_link.url = url
        
        await sync_to_async(social_link.full_clean)()
        await sync_to_async(social_link.save)()
        
        return social_link
    except Exception as e:
        logger.error(f"Error updating social link: {str(e)}")
        raise

async def delete_social_link(link_id: int) -> None:
    """Delete a social link"""
    try:
        social_link = await sync_to_async(get_object_or_404)(SocialLink, id=link_id)
        await sync_to_async(social_link.delete)()
    except Exception as e:
        logger.error(f"Error deleting social link: {str(e)}")
        raise

async def get_social_link(link_id: int) -> SocialLink:
    """Get a specific social link"""
    try:
        return await sync_to_async(get_object_or_404)(SocialLink, id=link_id)
    except Exception as e:
        logger.error(f"Error getting social link: {str(e)}")
        raise

async def get_profile_social_links(profile_id: int) -> list[SocialLink]:
    """Get all social links for a profile"""
    try:
        return await sync_to_async(list)(
            SocialLink.objects.filter(user_profile_id=profile_id).order_by('platform')
        )
    except Exception as e:
        logger.error(f"Error getting profile social links: {str(e)}")
        raise