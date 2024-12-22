from typing import List
from ninja import Router
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
from profiles.api.helpers.auth import check_auth_and_access

router = Router(tags=["skills"])

@router.get("/skills", response=List[SkillResponse])
async def list_skills(request):
    """List all available skills"""
    return await get_all_skills()

@router.post("/skills", response=SkillResponse)
async def create_new_skill(request, data: SkillCreate):
    """Create a new skill"""
    if not request.user.is_authenticated:
        raise ValueError("Authentication required")
    return await create_skill(data.name)

@router.get("/skills/{skill_id}", response=SkillResponse)
async def get_skill_by_id(request, skill_id: int):
    """Get a specific skill"""
    return await get_skill(skill_id)

@router.put("/skills/{skill_id}", response=SkillResponse)
async def update_skill_by_id(request, skill_id: int, data: SkillUpdate):
    """Update a skill"""
    if not request.user.is_authenticated:
        raise ValueError("Authentication required")
    if not request.user.is_staff:
        raise ValueError("Staff access required to update skills")
    return await update_skill(skill_id, data.name)

@router.delete("/skills/{skill_id}")
async def delete_skill_by_id(request, skill_id: int):
    """Delete a skill"""
    if not request.user.is_authenticated:
        raise ValueError("Authentication required")
    if not request.user.is_staff:
        raise ValueError("Staff access required to delete skills")
    await delete_skill(skill_id)
    return {"success": True}

@router.get("/{profile_id}/skills", response=List[SkillResponse])
async def get_profile_skills(request, profile_id: int):
    """Get skills for a specific profile"""
    profile = await check_auth_and_access(request, profile_id)
    return [skill async for skill in profile.skills.all()]

@router.put("/{profile_id}/skills")
async def update_profile_skills_endpoint(request, profile_id: int, data: ProfileSkillsUpdate):
    """Update skills for a specific profile"""
    profile = await check_auth_and_access(request, profile_id)
    await update_profile_skills(profile, data.skill_ids)
    return {"success": True} 