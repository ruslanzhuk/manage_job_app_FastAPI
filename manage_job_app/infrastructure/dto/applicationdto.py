from datetime import datetime
from typing import Optional, Literal

from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from manage_job_app.infrastructure.dto.job_categorydto import CategoryDTO
from manage_job_app.infrastructure.dto.locationdto import CitySimpleDTO
from manage_job_app.infrastructure.dto.offerdto import OfferDTO
from manage_job_app.infrastructure.dto.userdto import EmployeeDTO, EmployerDTO


class ApplicationDTO(BaseModel):
    """A model representing DTO for application data."""
    id: int
    offer_id: OfferDTO
    user_id: EmployeeDTO
    cover_letter: Optional[str] = None
    status: Literal["sent", "under_review", "accepted", "rejected"] = "sent"
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ApplicationDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ApplicationDTO: The final DTO instance.
        """
        record_dict = dict(record)
        print(record_dict)

        city_data_present_1 = record_dict.get("id_6") is not None and record_dict.get("name_4") is not None
        city_data_present_2 = record_dict.get("id_7") is not None and record_dict.get("name_5") is not None

        return cls(
            id=record_dict.get("id"),
            offer_id=OfferDTO(
                id=record_dict.get("id_1"),
                title=record_dict.get("title"),
                description=record_dict.get("description"),
                category=CategoryDTO(
                    id=record_dict.get("id_2"),
                    name=record_dict.get("name"),
                ),
                job_title=record_dict.get("job_title"),
                salary=record_dict.get("salary"),
                location=CitySimpleDTO(
                    id=record_dict.get("id_3"),
                    name=record_dict.get("name_1"),
                    country_id=record_dict.get("country_id"),
                ),
                author_id=EmployerDTO(
                    id=record_dict.get("id_4"),
                    name=record_dict.get("name_2"),
                    email=record_dict.get("email"),
                    number=record_dict.get("number"),
                    city=CitySimpleDTO(
                        id=record_dict.get("id_6"),
                        name=record_dict.get("name_4"),
                        country_id=record_dict.get("country_id_1"),
                    ) if city_data_present_1 else None,
                    company_name=record_dict.get("company_name"),
                    created_at=record_dict.get("created_at_2"),
                    updated_at=record_dict.get("updated_at_2"),
                ),
                created_at=record_dict.get("created_at_1"),
                updated_at=record_dict.get("updated_at_1")
            ),
            user_id=EmployeeDTO(
                id=record_dict.get("id_5"),
                name=record_dict.get("name_3"),
                email=record_dict.get("email_1"),
                number=record_dict.get("number_1"),
                city=CitySimpleDTO(
                    id=record_dict.get("id_7"),
                    name=record_dict.get("name_5"),
                    country_id=record_dict.get("country_id_2"),
                ) if city_data_present_2 else None,
                skills=record_dict.get("skills"),
                created_at=record_dict.get("created_at_3"),
                updated_at=record_dict.get("updated_at_3"),
            ),
            cover_letter=record_dict.get("cover_letter"),
            status=record_dict.get("status"),
            created_at=record_dict.get("created_at"),
            updated_at=record_dict.get("updated_at"),
        )

