from typing import List, Optional
from ninja import Schema
from pydantic import validator
from profiles.models.equal_employment import EqualEmploymentData

class YesNoValue(Schema):
    value: str

    @validator('value')
    def validate_yes_no(cls, v):
        if v not in ['Yes', 'No']:
            raise ValueError("Value must be 'Yes' or 'No'")
        return v

class YesNoDeclineValue(Schema):
    value: str

    @validator('value')
    def validate_yes_no_decline(cls, v):
        if v not in ['Yes', 'No', 'Decline to state']:
            raise ValueError("Value must be 'Yes', 'No', or 'Decline to state'")
        return v

class GenderValue(Schema):
    value: str

    @validator('value')
    def validate_gender(cls, v):
        if v not in ['Male', 'Female', 'Non-Binary', 'Decline to state']:
            raise ValueError("Invalid gender value")
        return v

class EthnicitiesValue(Schema):
    values: List[str]

    @validator('values')
    def validate_ethnicities(cls, v):
        valid_ethnicities = dict(EqualEmploymentData.ETHNICITY_CHOICES).keys()
        for ethnicity in v:
            if ethnicity not in valid_ethnicities:
                raise ValueError(f"Invalid ethnicity: {ethnicity}")
        return v

# Response Schemas
class YesNoResponse(YesNoValue):
    pass

class YesNoDeclineResponse(YesNoDeclineValue):
    pass

class GenderResponse(GenderValue):
    pass

class EthnicitiesResponse(EthnicitiesValue):
    is_hispanic_latinx: bool

class EqualEmploymentSummary(Schema):
    authorized_us: str
    authorized_canada: str
    authorized_uk: str
    requires_sponsorship: str
    ethnicities: List[str]
    is_hispanic_latinx: bool
    gender: str
    has_disability: str
    is_lgbtq: str
    is_veteran: str

class CompletionStatus(Schema):
    work_auth_complete: bool
    demographics_complete: bool
    additional_info_complete: bool
    all_complete: bool
    missing_fields: List[str]