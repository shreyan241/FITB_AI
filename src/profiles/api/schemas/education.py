from typing import Optional
from ninja import ModelSchema, Schema
from profiles.models.education import Education
from datetime import datetime
from enum import Enum

class DegreeType(str, Enum):
    """Enum for degree types matching Education model choices"""
    HIGH_SCHOOL = "High School"
    ASSOCIATES = "Associate's"
    BACHELORS = "Bachelor's"
    MASTERS = "Master's"
    PHD = "PhD"
    MBA = "MBA"
    MD = "MD"
    JD = "JD"
    BOOTCAMP = "Bootcamp"
    CERTIFICATION = "Certification"
    OTHER = "Other"

    @classmethod
    def choices(cls):
        """Get choices for Django model"""
        return [(member.value, member.value) for member in cls]

class EducationBase(Schema):
    """Base schema for education with common fields"""
    school_name: str
    degree_type: DegreeType
    major: Optional[str] = None
    minor: Optional[str] = None
    start_month: int
    start_year: int
    end_month: Optional[int] = None
    end_year: Optional[int] = None
    is_current: bool = False
    gpa: Optional[float] = None

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
                raise ValueError("Current education cannot have end dates")
            return data

        # If not current, validate end dates exist and are valid
        if not data.get('is_current'):
            if data.get('end_month') is None or data.get('end_year') is None:
                raise ValueError("End dates are required for completed education")
            
            start_date = datetime(data['start_year'], data['start_month'], 1)
            end_date = datetime(data['end_year'], data['end_month'], 1)
            if start_date > end_date:
                raise ValueError("Start date must be before end date")

        return data

class EducationCreate(EducationBase):
    """Schema for creating a new education entry"""
    def validate_dates(self):
        """Validate dates before creation"""
        return EducationBase.validate_dates(self.dict())

class EducationUpdate(Schema):
    """Schema for updating an education entry"""
    school_name: Optional[str] = None
    degree_type: Optional[DegreeType] = None
    major: Optional[str] = None
    minor: Optional[str] = None
    start_month: Optional[int] = None
    start_year: Optional[int] = None
    end_month: Optional[int] = None
    end_year: Optional[int] = None
    is_current: Optional[bool] = None
    gpa: Optional[float] = None

    def validate_dates(self, existing_data: dict):
        """Validate dates with existing data"""
        data = {**existing_data, **self.dict(exclude_unset=True)}
        return EducationBase.validate_dates(data)

class EducationResponse(ModelSchema):
    """Schema for education response"""
    class Config:
        model = Education
        model_fields = [
            'id',
            'school_name',
            'degree_type',
            'major',
            'minor',
            'start_month',
            'start_year',
            'end_month',
            'end_year',
            'is_current',
            'gpa'
        ] 