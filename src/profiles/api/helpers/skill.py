from typing import List
from django.db import IntegrityError
from profiles.models.skill import Skill
from profiles.models.user_profile import UserProfile
from better_profanity import profanity
from django.core.exceptions import ValidationError

# Configure profanity filter
profanity.load_censor_words()

async def create_skill(name: str) -> Skill:
    """Create a new skill, handling duplicates gracefully"""
    # Validate name for offensive content
    if profanity.contains_profanity(name.strip()):
        raise ValidationError("Skill name contains inappropriate content")
        
    try:
        return await Skill.objects.acreate(name=name.strip())
    except IntegrityError:
        # If skill already exists, return existing one
        return await Skill.objects.aget(name=name.strip())

async def update_skill(skill_id: int, name: str) -> Skill:
    """Update a skill's name"""
    # Validate name for offensive content
    if profanity.contains_profanity(name.strip()):
        raise ValidationError("Skill name contains inappropriate content")
        
    skill = await Skill.objects.aget(id=skill_id)
    skill.name = name.strip()
    try:
        await skill.asave()
        return skill
    except IntegrityError:
        raise ValueError("A skill with this name already exists")

async def delete_skill(skill_id: int) -> None:
    """Delete a skill if it's not being used"""
    skill = await Skill.objects.aget(id=skill_id)
    # Check if skill is being used by any profiles
    if await skill.userprofile_set.aexists():
        raise ValueError("Cannot delete skill that is being used by profiles")
    await skill.adelete()

async def get_skill(skill_id: int) -> Skill:
    """Get a skill by ID"""
    return await Skill.objects.aget(id=skill_id)

async def get_all_skills() -> List[Skill]:
    """Get all skills"""
    return [skill async for skill in Skill.objects.all()]

async def update_profile_skills(profile: UserProfile, skill_ids: List[int]) -> None:
    """Update a profile's skills"""
    # Verify all skills exist
    skills = []
    for skill_id in skill_ids:
        try:
            skill = await Skill.objects.aget(id=skill_id)
            skills.append(skill)
        except Skill.DoesNotExist:
            raise ValueError(f"Skill with ID {skill_id} does not exist")
    
    # Update profile's skills
    profile.skills.set(skills)
    await profile.asave() 