"""Module containing city database repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from manage_job_app.core.domain.location import City, CityIn
from manage_job_app.core.repositories.icity import ICityRepository
from manage_job_app.db import city_table, database, country_table, continent_table
from manage_job_app.infrastructure.dto.locationdto import CityDTO


class CityRepository(ICityRepository):
    """A class implementing the city repository."""

    async def get_all_cities(self) -> Iterable[Any]:
        """The method getting all cities from the data storage.

        Returns:
            Iterable[Any]: The collection of the all cities.
        """

        query = city_table.select().order_by(city_table.c.name.asc())
        cities = await database.fetch_all(query)

        return [City(**dict(city)) for city in cities]

    async def get_city_by_id(self, city_id: int) -> Any | None:
        """The method getting a city from the data storage.

        Args:
            city_id (int): The id of the city.

        Returns:
            Any | None: The city data if exists.
        """

        city = await self._get_by_id(city_id)

        return CityDTO.from_record(city) if city else None

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

        query = city_table.select().where(city_table.c.country_id == country_id).order_by(city_table.c.name.asc())
        cities = await database.fetch_all(query)

        return [City(**dict(city)) for city in cities]


    async def add_city(self, data: CityIn) -> Any | None:
        """The method adding new city to the data storage.

        Args:
            data (CityIn): The attributes of the city.

        Returns:
            Any | None: The newly created city.
        """

        query = city_table.insert().values(**data.model_dump())
        new_city_id = await database.execute(query)
        new_city = await self._get_by_id(new_city_id)

        return City(**dict(new_city)) if new_city else None

    async def update_city(
        self,
        city_id: int,
        data: CityIn,
    ) -> Any | None:
        """The method updating city data in the data storage.

        Args:
            city_id (int): The city id.
            data (CityIn): The attributes of the city.

        Returns:
            Any | None: The updated city.
        """

        if self._get_by_id(city_id):
            query = (
                city_table.update()
                .where(city_table.c.id == city_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            city = await self._get_by_id(city_id)

            return City(**dict(city)) if city else None

        return None

    async def delete_city(self, city_id: int) -> bool:
        """The method updating removing city from the data storage.

        Args:
            city_id (int): The city id.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(city_id):
            query = city_table \
                .delete() \
                .where(city_table.c.id == city_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, city_id: int) -> Record | None:
        """A private method getting city from the DB based on its ID.

        Args:
            city_id (int): The ID of the city.

        Returns:
            Any | None: city record if exists.
        """

        query = (
            select(city_table, country_table, continent_table)
            .select_from(
                join(
                    city_table,
                    country_table,
                    city_table.c.country_id == country_table.c.id
                ).join(
                    continent_table,
                    country_table.c.continent_id == continent_table.c.id
                )
            ).where(city_table.c.id == city_id)
        )


        return await database.fetch_one(query)