"""A module containing DTO models for output offers."""

from datetime import datetime
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

from manage_job_app.infrastructure.dto.job_categorydto import CategoryDTO
from manage_job_app.infrastructure.dto.locationdto import CitySimpleDTO
from manage_job_app.infrastructure.dto.userdto import EmployerDTO


class OfferDTO(BaseModel):
    """A model representing DTO for offer data."""
    id: int
    title: str
    description: str
    category: CategoryDTO
    job_title: str
    salary: int
    location: CitySimpleDTO
    author_id: EmployerDTO
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "OfferDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            OfferDTO: The final DTO instance.
        """
        record_dict = dict(record)

        city_data_present = record_dict.get("id_4") is not None and record_dict.get("name_3") is not None

        return cls(
            id=record_dict.get("id"),
            title=record_dict.get("title"),
            description=record_dict.get("description"),
            category=CategoryDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name")
            ),
            job_title=record_dict.get("job_title"),
            salary=record_dict.get("salary"),
            location=CitySimpleDTO(
                id=record_dict.get("id_2"),
                name=record_dict.get("name_1"),
                country_id=record_dict.get("country_id"),
            ),

            author_id=EmployerDTO(
                id=record_dict.get("id_3"),
                name=record_dict.get("name_2"),
                email=record_dict.get("email"),
                number=record_dict.get("number"),
                city=CitySimpleDTO(
                    id=record_dict.get("id_4"),
                    name=record_dict.get("name_3"),
                    country_id=record_dict.get("country_id_1"),
                ) if city_data_present else None,
                company_name=record_dict.get("company_name"),
                created_at=record_dict.get("created_at_1"),
                updated_at=record_dict.get("updated_at_1"),
            ),
            created_at=record_dict.get("created_at"),
            updated_at=record_dict.get("updated_at"),
        )