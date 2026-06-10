"""Module containing city service implementation."""

from typing import Iterable


from manage_job_app.core.domain.location import City, CityIn
from manage_job_app.core.repositories.icity import ICityRepository
from manage_job_app.infrastructure.dto.locationdto import CityDTO
from manage_job_app.infrastructure.services.icity import ICityService


class CityService(ICityService):
    """A class implementing the city service."""

    _repository: ICityRepository

    def __init__(self, repository: ICityRepository) -> None:
        """The initializer of the `city service`.

        Args:
            repository (ICityRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all_cities(self) -> Iterable[City]:
        """The method getting all countries from the repository.

        Returns:
            Iterable[City]: The collection of the all countries.
        """

        return await self._repository.get_all_cities()

    async def get_city_by_id(self, city_id: int) -> CityDTO | None:
        """The method getting a city from the repository.

        Args:
            city_id (int): The id of the city.

        Returns:
            City | None: The city data if exists.
        """

        return await self._repository.get_city_by_id(city_id)

    async def get_cities_by_country(
            self,
            country_id: int,
    ) -> Iterable[City]:
        """The abstract getting all provided country's cities
            from the repository.

        Args:
            country_id (int): The id of the country.

        Returns:
            Iterable[City]: The collection of the cities.
        """

        return await self._repository.get_cities_by_country(country_id)


    async def add_city(self, data: CityIn) -> City | None:
        """The method adding new city to the repository.

        Args:
            data (CityIn): The attributes of the city.

        Returns:
            City | None: The newly created city.
        """

        return await self._repository.add_city(data)

    async def update_city(
        self,
        city_id: int,
        data: CityIn,
    ) -> City | None:
        """The method updating city data in the repository.

        Args:
            city_id (int): The city id.
            data (CityIn): The attributes of the city.

        Returns:
            City | None: The updated city.
        """

        return await self._repository.update_city(
            city_id=city_id,
            data=data,
        )

    async def delete_city(self, city_id: int) -> bool:
        """The method updating removing city from the repository.

        Args:
            city_id (int): The city id.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_city(city_id)