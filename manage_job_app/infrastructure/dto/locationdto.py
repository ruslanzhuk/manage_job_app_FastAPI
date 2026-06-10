"""A module containing DTO models for country."""
from asyncpg import Record
from pydantic import BaseModel, ConfigDict  # type: ignore

#from manage_job_app.core.domain.location import Continent

class ContinentDTO(BaseModel):
    """A model representing DTO for continent data."""
    id: int
    name: str
    alias: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )


class CountryDTO(BaseModel):
    """A model representing DTO for country data."""
    id: int
    name: str
    alias: str
    continent: ContinentDTO

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

class CitySimpleDTO(BaseModel):
    """A model representing DTO for simple city data."""
    id: int
    name: str
    country_id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "CitySimpleDTO":
        """A method to create an CityDTO instance from a DB record.

        Args:
            record (Record): The DB record.

        Returns:
            CitySimpleDTO: The final DTO instance.
        """

        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
            country_id=record_dict.get("country_id")
        )

class CityDTO(BaseModel):
    """A model representing DTO for city data."""
    id: int
    name: str
    country_id: CountryDTO

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "CityDTO":
        """A method to create an CityDTO instance from a DB record.

        Args:
            record (Record): The DB record.

        Returns:
            CitySimpleDTO: The final DTO instance.
        """

        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
            country_id=CountryDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name_1"),
                alias=record_dict.get("alias"),
                continent=ContinentDTO(
                    id=record_dict.get("id_2"),
                    name=record_dict.get("name_2"),
                    alias=record_dict.get("alias_1"),
                ),
            ),
        )