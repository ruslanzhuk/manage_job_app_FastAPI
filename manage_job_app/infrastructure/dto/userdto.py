"""A module containing DTO models for output users."""

from datetime import datetime
from typing import Optional, List
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4

from manage_job_app.infrastructure.dto.locationdto import CitySimpleDTO


class EmployerDTO(BaseModel):
    """A model representing DTO for employer data."""
    id: UUID4
    name: str
    email: str
    number: Optional[str] = None
    city: Optional[CitySimpleDTO] = None
    company_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore", arbitrary_types_allowed=True)

    @classmethod
    def from_record(cls, record: Record) -> "EmployerDTO":
        """A method to create an EmployerDTO instance from a DB record.

        Args:
            record (Record): The DB record.

        Returns:
            EmployerDTO: The final DTO instance.
        """

        record_dict = dict(record)

        city_data_present = record_dict.get("id_1") is not None and record_dict.get("name_1") is not None

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
            email=record_dict.get("email"),
            number=record_dict.get("number"),
            city=CitySimpleDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name_1"),
                country_id=record_dict.get("country_id")
            ) if city_data_present else None,
            company_name=record_dict.get("company_name"),
            created_at=record_dict.get("created_at"),
            updated_at=record_dict.get("updated_at")
        )


class EmployeeDTO(BaseModel):
    """A model representing DTO for employee data."""
    id: UUID4
    name: str
    email: str
    number: Optional[str] = None
    city: Optional[CitySimpleDTO] = None
    skills: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore", arbitrary_types_allowed=True)

    @classmethod
    def from_record(cls, record: Record) -> "EmployeeDTO":
        """A method to create an EmployeeDTO instance from a DB record.

        Args:
            record (Record): The DB record.

        Returns:
            EmployeeDTO: The final DTO instance.
        """


        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
            email=record_dict.get("email"),
            number=record_dict.get("number"),
            city=CitySimpleDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name_1"),
                country_id=record_dict.get("country_id")
            ),
            skills=record_dict.get("skills"),
            created_at=record_dict.get("created_at"),
            updated_at=record_dict.get("updated_at")
        )

