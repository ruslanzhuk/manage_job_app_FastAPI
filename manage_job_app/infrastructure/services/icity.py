"""Module containing city service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from manage_job_app.core.domain.location import City, CityIn
from manage_job_app.infrastructure.dto.locationdto import CityDTO


class ICityService(ABC):
    """An abstract class representing protocol of city repository."""

    @abstractmethod
    async def get_all_cities(self) -> Iterable[City]:
        """The abstract getting all cities from the repository.

        Returns:
            Iterable[city]: The collection of the all cities.
        """

    @abstractmethod
    async def get_city_by_id(self, city_id: int) -> CityDTO | None:
        """The abstract getting a city from the repository.

        Args:
            city_id (int): The id of the city.

        Returns:
            city | None: The city data if exists.
        """

    @abstractmethod
    async def get_cities_by_country(
            self,
            country_id: int,
    ) -> Iterable[City]:
        """The abstract getting all provided country's cities
            from the repository.

        Args:
            country_id (int): The id of the country.

        Returns:
            Iterable[city]: The collection of the cities.
        """

    @abstractmethod
    async def add_city(self, data: CityIn) -> City | None:
        """The abstract adding new city to the repository.

        Args:
            data (CityIn): The attributes of the city.

        Returns:
            City | None: The newly created city.
        """

    @abstractmethod
    async def update_city(
        self,
        city_id: int,
        data: CityIn,
    ) -> City | None:
        """The abstract updating city data in the repository.

        Args:
            city_id (int): The city id.
            data (CityIn): The attributes of the city.

        Returns:
            City | None: The updated city.
        """

    @abstractmethod
    async def delete_city(self, city_id: int) -> bool:
        """The abstract updating removing city from the repository.

        Args:
            city_id (int): The city id.

        Returns:
            bool: Success of the operation.
        """