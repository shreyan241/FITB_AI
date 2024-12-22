from typing import Optional, List
from ninja import ModelSchema, Schema
from profiles.models.skill import Skill
from better_profanity import profanity

# Configure profanity filter
profanity.load_censor_words()

class SkillBase(Schema):
    """Base schema for skill with common fields"""
    name: str

    @staticmethod
    def validate_name(data):
        """Validate skill name"""
        name = data['name'].strip()
        if not name:
            raise ValueError("Skill name cannot be empty")
        if len(name) > 100:
            raise ValueError("Skill name too long (max 100 characters)")
        
        # Check for offensive content
        if profanity.contains_profanity(name):
            raise ValueError("Skill name contains inappropriate content")
            
        return {**data, 'name': name}  # Return normalized name

class SkillCreate(SkillBase):
    """Schema for creating a new skill"""
    pass

class SkillUpdate(Schema):
    """Schema for updating a skill"""
    name: Optional[str] = None

    def validate_name(self, existing_data: dict):
        """Validate name if provided"""
        if self.name is not None:
            return SkillBase.validate_name({'name': self.name})
        return existing_data

class SkillResponse(ModelSchema):
    """Schema for skill response"""
    class Config:
        model = Skill
        model_fields = ['id', 'name', 'created_at', 'updated_at']

class ProfileSkillsUpdate(Schema):
    """Schema for updating a profile's skills"""
    skill_ids: List[int] 