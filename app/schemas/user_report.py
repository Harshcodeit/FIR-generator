from pydantic import BaseModel, Field ,field_validator # Field enfroce advance constraints,guides ai using desc
from typing import List,Optional

class UserReportSchema(BaseModel):
    # 1. Incident Details (What happened)
    offence_description: str = Field(
        description="A plain-text description of what happened (e.g., 'Bank Fraud', 'Stolen Wallet', 'Online Scam')"
    )
    
    # 2. Timeline (When it happened)
    offence_date: Optional[str] = Field(
        default=None,
        description="The date or date-range when the incident took place (e.g., 'Tuesday', 'Between 2014 and 2016')"
    )
    offence_time: Optional[str] = Field(
        default=None,
        description="The time of day the incident occurred if known"
    )

    # 3. Location (Where it happened)
    location_name: Optional[str] = Field(
        default=None,
        description="The name of the house, business, shop, or street where it occurred (e.g., 'Lenin Sarani')"
    )
    landmark : Optional[str] = Field(
        default=None,
        description="A landmark close to the incident point"
    )
    city: Optional[str] = Field(
        default=None,
        description="The city or town name"
    )
    state: Optional[str] = Field(
        default=None,
        description="The state name"
    )
    
    # 4. User Information (Who is reporting)
    reporter_full_name: Optional[str] = Field(
        default=None,
        description="Full name of complainant"
    )
    father_or_husband_name : Optional[str] = Field(
        default = None,
        description = "Name of father or husband of complainant"
    )
    dob : Optional[str] = Field(
        default = None,
        description = "Date of birth of complainant"
    )
    nationality : Optional[str] = Field(
        default = None,
        description = "Nationality of complainant"
    )
    occupation : Optional[str] = Field(
        default = None,
        description = "Occupation of complainant"
    )
    address: Optional[str] = Field(
        default=None,
        description="Address of the complainant"
    )
    phone_number : Optional[str] = Field(
        default = None,
        description="Phone number of the complainant"
    )
    delay_reason: Optional[str] = Field(
        default=None,
        description="Reasons given by complainant to file a report late"
    )

    # 5.Accused Information
    accused_description: Optional[str] = Field(
        default=None,
        description="Description of the accused person"
    )

    # 6.Property
    property_type: Optional[str] = Field(
        default=None,
        description="Particulars of properties stolen or involved"
    )
    estimated_value: Optional[str] = Field(
        default=None,
        description="Total value of the properties stolen / involved"
    )
    
    
    @field_validator('*',mode='before') # decorators are functions used to modify other functions - wrapper
    @classmethod
    def clean_placeholders(cls,value):
        INVALID_VALUES = {
            "Not provided",
            "Not mentioned",
            "Unknown",
            "N/A",
            "ReporterName",
            "CityName",
            "StateName",
            "Occupation"
        }

        if isinstance(value,str) and value.strip() in INVALID_VALUES:
            return None
        
        return value
