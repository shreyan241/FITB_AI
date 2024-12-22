from typing import Optional
from ninja import ModelSchema, Schema
from profiles.models.work_experience import WorkExperience
from datetime import datetime
from enum import Enum

class EmploymentType(str, Enum):
    """Enum for employment types matching WorkExperience model choices"""
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    TEMPORARY = "Temporary"
    INTERNSHIP = "Internship"
    APPRENTICESHIP = "Apprenticeship"
    FREELANCE = "Freelance"
    VOLUNTEER = "Volunteer"
    OTHER = "Other"

    @classmethod
    def choices(cls):
        """Get choices for Django model"""
        return [(member.value, member.value) for member in cls]

class WorkExperienceBase(Schema):
    """Base schema for work experience with common fields"""
    company: str
    position_title: str
    employment_type: EmploymentType
    city: str
    state: str
    country: str
    is_remote: bool = False
    start_month: int
    start_year: int
    end_month: Optional[int] = None
    end_year: Optional[int] = None
    is_current: bool = False
    description: str

    @staticmethod
    def validate_dates(data):
        """Validate dates based on is_current status and date order"""
        # Validate month ranges
        if not 1 <= data['start_month'] <= 12:
            raise ValueError("Start month must be between 1 and 12")
        if data.get('end_month') and not 1 <= data['end_month'] <= 12:
            raise ValueError("End month must be between 1 and 12")

        # If is_current is True, end dates must be None
        if data.get('is_current'):
            if data.get('end_month') is not None or data.get('end_year') is not None:
                raise ValueError("Current positions cannot have end dates")
            return data

        # If not current, validate end dates exist and are valid
        if not data.get('is_current'):
            if data.get('end_month') is None or data.get('end_year') is None:
                raise ValueError("End dates are required for non-current positions")
            
            start_date = datetime(data['start_year'], data['start_month'], 1)
            end_date = datetime(data['end_year'], data['end_month'], 1)
            if start_date > end_date:
                raise ValueError("Start date must be before end date")

        return data

class WorkExperienceCreate(WorkExperienceBase):
    """Schema for creating a new work experience entry"""
    def validate_dates(self):
        """Validate dates before creation"""
        return WorkExperienceBase.validate_dates(self.dict())

class WorkExperienceUpdate(Schema):
    """Schema for updating a work experience entry"""
    company: Optional[str] = None
    position_title: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    is_remote: Optional[bool] = None
    start_month: Optional[int] = None
    start_year: Optional[int] = None
    end_month: Optional[int] = None
    end_year: Optional[int] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None

    def validate_dates(self, existing_data: dict):
        """Validate dates with existing data"""
        data = {**existing_data, **self.dict(exclude_unset=True)}
        return WorkExperienceBase.validate_dates(data)

class WorkExperienceResponse(ModelSchema):
    """Schema for work experience response"""
    class Config:
        model = WorkExperience
        model_fields = [
            'id',
            'company',
            'position_title',
            'employment_type',
            'city',
            'state',
            'country',
            'is_remote',
            'start_month',
            'start_year',
            'end_month',
            'end_year',
            'is_current',
            'description'
        ] 