""" Module containing city repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from manage_job_app.core.domain.location import CityIn


class ICityRepository(ABC):
    """An abstract class representing protocol of city repository."""

    @abstractmethod
    async def get_all_cities(self) -> Iterable[Any]:
        """The abstract getting all cities from the data storage.

        Returns:
            Iterable[Any]: The collection of the all cities.
        """

    @abstractmethod
    async def get_city_by_id(self, city_id: int) -> Any | None:
        """The abstract getting a city from the data storage.

        Args:
            city_id (int): The id of the city.

        Returns:
            Any | None: The city data if exists.
        """

    @abstractmethod
    async def get_cities_by_country(
            self,
            country_id: int,
    ) -> Iterable[Any]:
        """The abstract getting all provided country's cities
            from the data storage.

        Args:
            country_id (int): The id of the country.

        Returns:
            Iterable[Any]: The collection of the cities.
        """

    @abstractmethod
    async def add_city(self, data: CityIn) -> Any | None:
        """The abstract adding new city to the data storage.

        Args:
            data (CityIn): The attributes of the city.

        Returns:
            Any | None: The newly created city.
        """

    @abstractmethod
    async def update_city(
            self,
            city_id: int,
            data: CityIn,
    ) -> Any | None:
        """The abstract updating city data in the data storage.

        Args:
            city_id (int): The id of the city.
            data (CityIn): The details of the updated city.

        Returns:
            Any | None: The updated city details.
        """

    @abstractmethod
    async def delete_city(self, city_id: int) -> bool:
        """The abstract updating removing city from the data storage.

        Args:
            city_id (int): The id of the city.

        Returns:
            bool: Success of the operation.
        """