"""A model containing user-related models."""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, UUID1, UUID4


class UserIn(BaseModel):
    """Model representing user's DTO attributes."""
    name: str
    email: str
    password: str
    number: Optional[str] = None
    city: Optional[int] = None

class EmployerIn(UserIn):
    """Model representing employer's DTO attributes."""
    company_name: Optional[str] = None

class Employer(EmployerIn):
    """The employer model class."""
    id: UUID4

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class EmployeeIn(UserIn):
    """Model representing employee's DTO attributes."""
    skills: Optional[List[str]] = None

class Employee(EmployeeIn):
    """The employee model class."""
    id: UUID4

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")
