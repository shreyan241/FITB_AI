from typing import List
from ninja import Router
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models import Case, When, Value, IntegerField
from profiles.api.schemas.skill import (
    SkillCreate,
    SkillUpdate,
    SkillResponse,
    ProfileSkillsUpdate
)
from profiles.api.helpers.skill import (
    create_skill,
    update_skill,
    delete_skill,
    get_skill,
    get_all_skills,
    update_profile_skills
)
from profiles.api.helpers.auth import check_auth_and_access, check_auth_and_staff, get_profile_with_auth_check
from asgiref.sync import sync_to_async
from profiles.utils.logger.logging_config import logger
from django.db.models import Q
from profiles.models import Skill

router = Router(tags=["skills"])

# Global skill management endpoints (must come before parameterized routes)
@router.get("/skills/all", response=List[SkillResponse])
async def list_skills(request):
    """List all available skills"""
    # Just check authentication
    if not await sync_to_async(lambda: request.user.is_authenticated)():
        raise PermissionDenied("Authentication required")
    return await get_all_skills()

@router.get("/skills/search", response=List[SkillResponse])
async def search_skills(
    request,
    query: str,
    limit: int = 10,
    offset: int = 0
):
    """
    Search for skills based on a query string.
    Returns paginated results of skills that match the query.
    The search is case-insensitive and matches partial names.
    """
    # Check authentication
    if not await sync_to_async(lambda: request.user.is_authenticated)():
        raise PermissionDenied("Authentication required")

    try:
        # Validate parameters
        if limit < 1 or limit > 100:
            raise ValidationError("Limit must be between 1 and 100")
        if offset < 0:
            raise ValidationError("Offset must be non-negative")

        # Create a case-insensitive query that matches the start of the name
        # or matches anywhere in the name, with proper ordering
        skills = await sync_to_async(lambda: list(
            Skill.objects.filter(
                Q(name__istartswith=query) | Q(name__icontains=query)
            ).annotate(
                # Add a priority field to sort by
                match_priority=Case(
                    When(name__istartswith=query, then=Value(1)),
                    default=Value(2),
                    output_field=IntegerField(),
                )
            ).order_by('match_priority', 'name')[offset:offset + limit]
        ))()

        # Convert to list of SkillResponse
        return [
            SkillResponse(
                id=skill.id,
                name=skill.name,
                created_at=skill.created_at,
                updated_at=skill.updated_at
            ) for skill in skills
        ]
    except ValidationError as e:
        raise e
    except Exception as e:
        logger.error(f"Error searching skills: {str(e)}")
        raise ValidationError("An error occurred while searching for skills")

@router.post("/skills/new", response=SkillResponse)
async def create_new_skill(request, data: SkillCreate):
    """Create a new skill"""
    # Just check authentication
    if not await sync_to_async(lambda: request.user.is_authenticated)():
        raise PermissionDenied("Authentication required")
    
    try:
        return await create_skill(data.name)
    except Exception as e:
        logger.error(f"Error creating skill: {str(e)}")
        raise ValidationError("Failed to create skill")

@router.get("/skills/{skill_id}", response=SkillResponse)
async def get_skill_by_id(request, skill_id: int):
    """Get a specific skill"""
    # Just check authentication
    if not await sync_to_async(lambda: request.user.is_authenticated)():
        raise PermissionDenied("Authentication required")
    
    try:
        return await get_skill(skill_id)
    except Exception as e:
        logger.error(f"Error getting skill: {str(e)}")
        raise ValidationError("Failed to get skill")

@router.put("/skills/{skill_id}", response=SkillResponse)
async def update_skill_by_id(request, skill_id: int, data: SkillUpdate):
    """Update a skill (staff only)"""
    # Check staff access
    await check_auth_and_staff(request)
    
    try:
        return await update_skill(skill_id, data.name)
    except Exception as e:
        logger.error(f"Error updating skill: {str(e)}")
        raise ValidationError("Failed to update skill")

@router.delete("/skills/{skill_id}")
async def delete_skill_by_id(request, skill_id: int):
    """Delete a skill (staff only)"""
    # Check staff access
    await check_auth_and_staff(request)
    
    try:
        await delete_skill(skill_id)
        return {"success": True}
    except Exception as e:
        logger.error(f"Error deleting skill: {str(e)}")
        raise ValidationError("Failed to delete skill")

# Profile-specific skill management (comes after global skill routes)
@router.get("/{profile_id}/skills", response=List[SkillResponse])
async def get_profile_skills(request, profile_id: int):
    """Get skills for a specific profile"""
    try:
        profile = await get_profile_with_auth_check(request, profile_id, "view skills for")
        return [skill async for skill in profile.skills.all()]
    except Exception as e:
        logger.error(f"Error getting profile skills: {str(e)}")
        raise ValidationError("Failed to get profile skills")

@router.put("/{profile_id}/skills")
async def update_profile_skills_endpoint(request, profile_id: int, data: ProfileSkillsUpdate):
    """Update skills for a specific profile"""
    try:
        profile = await get_profile_with_auth_check(request, profile_id, "update skills for")
        await update_profile_skills(profile, data.skill_ids)
        return {"success": True}
    except Exception as e:
        logger.error(f"Error updating profile skills: {str(e)}")
        raise ValidationError("Failed to update profile skills") 