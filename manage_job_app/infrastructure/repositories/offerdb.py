"""Module containing offer repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join, alias

from pydantic import UUID5

from manage_job_app.core.repositories.ioffer import IOfferRepository
from manage_job_app.core.domain.offer import Offer, OfferBroker
from manage_job_app.db import (
    offer_table,
    category_table,
    employer_table,
    city_table,
    database,
)
from manage_job_app.infrastructure.dto.offerdto import OfferDTO


class OfferRepository(IOfferRepository):
    """A class representing offer DB repository."""

    async def get_all_offers(self) -> Iterable[Any]:
        """The method getting all offers from the data storage.

        Returns:
            Iterable[Any]: Offers in the data storage.
        """

        city_offer_alias = alias(city_table, name="cities_offer")
        city_author_alias = alias(city_table, name="cities_author")

        query = (
            select(offer_table, category_table, city_offer_alias, employer_table, city_author_alias)
            .select_from(
                join(
                    offer_table,
                    category_table,
                    offer_table.c.category == category_table.c.id
                ).join(
                    city_offer_alias,
                    offer_table.c.location == city_offer_alias.c.id
                ).join(
                    employer_table,
                    offer_table.c.author_id == employer_table.c.id
                ).join(
                    city_author_alias,
                    employer_table.c.city == city_author_alias.c.id
                )
            )
            .order_by(offer_table.c.title.asc())
        )
        offers = await database.fetch_all(query)

        return [OfferDTO.from_record(offer) for offer in offers]


    async def get_by_id(self, offer_id: int) -> Any | None:
        """The method getting offer by provided id.

        Args:
            offer_id (int): The id of the offer.

        Returns:
            Any | None: The offer details.
        """

        city_offer_alias = alias(city_table, name="cities_offer")
        city_author_alias = alias(city_table, name="cities_author")

        query = (
            select(offer_table, category_table, city_offer_alias, employer_table, city_author_alias)
            .select_from(
                join(
                    offer_table,
                    category_table,
                    offer_table.c.category == category_table.c.id
                ).join(
                    city_offer_alias,
                    offer_table.c.location == city_offer_alias.c.id
                ).join(
                    employer_table,
                    offer_table.c.author_id == employer_table.c.id
                ).join(
                    city_author_alias,
                    employer_table.c.location == city_author_alias.c.id
                )
            )
            .where(offer_table.c.id == offer_id)
            .order_by(offer_table.c.title.asc())
        )
        offer = await database.fetch_one(query)

        return OfferDTO.from_record(offer) if offer else None


    async def get_by_user(self, user_id: UUID5) -> Iterable[Any]:
        """The method getting offers by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: The offer collection.
        """

        query = (
            select(offer_table)
            .where(offer_table.c.author_id == user_id)
            .order_by(offer_table.c.title.asc())
        )

        offers = await database.fetch_all(query)

        return [dict(offer) for offer in offers]

    async def search_by_title(self, title: str) -> Iterable[Any]:
        """Search for offers by title.

        Args:
            title (str): The title of the offer.

        Returns:
            Iterable[Any]: A collection of offers matching the title.
        """

        query = (
            select(offer_table)
            .where(offer_table.c.title.ilike(f"%{title}%"))  # Case-insensitive search
            .order_by(offer_table.c.title.asc())
        )

        offers = await database.fetch_all(query)

        return [dict(offer) for offer in offers]

    async def add_offer(self, data: OfferBroker) -> Any | None:
        """The method adding new offer to the data storage.

        Args:
            data (OfferBroker): The details of the new offer.

        Returns:
            Offer: Full details of the newly added offer.

        Returns:
            Any | None: The newly added offer.
        """

        query = offer_table.insert().values(**data.model_dump())
        new_offer_id = await database.execute(query)
        new_offer = await self._get_by_id(new_offer_id)

        return Offer(**dict(new_offer)) if new_offer else None

    async def update_offer(
        self,
        offer_id: int,
        data: OfferBroker,
    ) -> Any | None:
        """The method updating offer data in the data storage.

        Args:
            offer_id (int): The id of the offer.
            data (OfferIn): The details of the updated offer.

        Returns:
            Any | None: The updated offer details.
        """

        if self._get_by_id(offer_id):
            query = (
                offer_table.update()
                .where(offer_table.c.id == offer_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            offer = await self._get_by_id(offer_id)

            return Offer(**dict(offer)) if offer else None

        return None

    async def delete_offer(self, offer_id: int) -> bool:
        """The method updating removing offer from the data storage.

        Args:
            offer_id (int): The id of the offer.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(offer_id):
            query = offer_table \
                .delete() \
                .where(offer_table.c.id == offer_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, offer_id: int) -> Record | None:
        """A private method getting offer from the DB based on its ID.

        Args:
            offer_id (int): The ID of the offer.

        Returns:
            Any | None: Offer record if exists.
        """

        query = (
            offer_table.select()
            .where(offer_table.c.id == offer_id)
            .order_by(offer_table.c.title.asc())
        )

        return await database.fetch_one(query)