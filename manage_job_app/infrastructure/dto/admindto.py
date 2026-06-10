"""A module containing DTO models for output admins."""

from datetime import datetime
from typing import Optional, List
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4

class AdminDTO(BaseModel):
    """A model representing DTO for admin data."""
    id: UUID4
    email: str
    password: str
    privileges: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore", arbitrary_types_allowed=True)

    @classmethod
    def from_record(cls, record: Record) -> "AdminDTO":
        """A method to create an AdminDTO instance from a DB record.

        Args:
            record (Record): The DB record.

        Returns:
            AdminDTO: The final DTO instance.
        """

        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            email=record_dict.get("email"),
            password=record_dict.get("password"),
            privileges=record_dict.get("privileges"),
            created_at=record_dict.get("created_at"),
            updated_at=record_dict.get("updated_at"),
        )

