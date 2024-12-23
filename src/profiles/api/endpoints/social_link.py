from typing import List, Dict
from ninja import Router
from django.core.exceptions import ValidationError
from profiles.api.schemas.social_link import (
    SocialLinkCreate,
    SocialLinkUpdate
)
from profiles.api.helpers.social_link import (
    create_social_link,
    update_social_link,
    delete_social_link,
    get_social_link,
    get_profile_social_links
)
from profiles.api.helpers.auth import check_auth_and_access
from profiles.utils.logger.logging_config import logger

router = Router(tags=["social-links"])

def convert_social_link_to_response(social_link) -> dict:
    """Convert a social link model instance to a response dict"""
    return {
        "id": social_link.id,
        "platform": social_link.platform,
        "url": str(social_link.url)
    }

@router.get("/{profile_id}/social-links", response=List[Dict])
async def list_social_links(request, profile_id: int):
    """List all social links for a profile"""
    try:
        # Check authentication and access
        profile = await check_auth_and_access(request, profile_id)
        
        # Get social links
        social_links = await get_profile_social_links(profile_id)
        return [convert_social_link_to_response(link) for link in social_links]
    except Exception as e:
        logger.error(f"Error listing social links: {str(e)}")
        raise

@router.get("/{profile_id}/social-links/{link_id}", response=Dict)
async def get_social_link_by_id(request, profile_id: int, link_id: int):
    """Get a specific social link"""
    try:
        # Check authentication and access
        await check_auth_and_access(request, profile_id)
        
        # Get social link
        social_link = await get_social_link(link_id)
        
        # Verify link belongs to profile
        if social_link.user_profile_id != profile_id:
            raise ValidationError("Social link does not belong to this profile")
        
        return convert_social_link_to_response(social_link)
    except Exception as e:
        logger.error(f"Error getting social link: {str(e)}")
        raise

@router.post("/{profile_id}/social-links", response=Dict)
async def create_social_link_endpoint(request, profile_id: int, data: SocialLinkCreate):
    """Create a new social link"""
    try:
        # Check authentication and access
        profile = await check_auth_and_access(request, profile_id)
        
        # Create social link
        social_link = await create_social_link(
            profile=profile,
            platform=data.platform,
            url=str(data.url)  # Convert Pydantic HttpUrl to string
        )
        
        return convert_social_link_to_response(social_link)
    except Exception as e:
        logger.error(f"Error creating social link: {str(e)}")
        raise

@router.put("/{profile_id}/social-links/{link_id}", response=Dict)
async def update_social_link_endpoint(request, profile_id: int, link_id: int, data: SocialLinkUpdate):
    """Update a social link"""
    try:
        # Check authentication and access
        await check_auth_and_access(request, profile_id)
        
        # Get existing link to verify ownership
        existing_link = await get_social_link(link_id)
        if existing_link.user_profile_id != profile_id:
            raise ValidationError("Social link does not belong to this profile")
        
        # Update social link
        social_link = await update_social_link(
            link_id=link_id,
            platform=data.platform,
            url=str(data.url) if data.url else None
        )
        
        return convert_social_link_to_response(social_link)
    except Exception as e:
        logger.error(f"Error updating social link: {str(e)}")
        raise

@router.delete("/{profile_id}/social-links/{link_id}")
async def delete_social_link_endpoint(request, profile_id: int, link_id: int):
    """Delete a social link"""
    try:
        # Check authentication and access
        await check_auth_and_access(request, profile_id)
        
        # Get existing link to verify ownership
        existing_link = await get_social_link(link_id)
        if existing_link.user_profile_id != profile_id:
            raise ValidationError("Social link does not belong to this profile")
        
        # Delete social link
        await delete_social_link(link_id)
        return {"success": True}
    except Exception as e:
        logger.error(f"Error deleting social link: {str(e)}")
        raise