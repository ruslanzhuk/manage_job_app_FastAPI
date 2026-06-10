from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, UUID1, UUID4


class AdminIn(BaseModel):
    """Model representing admin's DTO attributes."""
    email: str
    password: str
    privileges: str

class Admin(AdminIn):
    """The admin model class."""
    id: UUID4

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")
