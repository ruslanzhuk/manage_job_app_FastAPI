"""Module containing job category database repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore

from manage_job_app.core.domain.job_category import Category, CategoryIn
from manage_job_app.core.repositories.ijob_category import ICategoryRepository
from manage_job_app.db import category_table, offer_table, database
from sqlalchemy import select, join
from manage_job_app.infrastructure.dto.job_categorydto import CategoryDTO


class CategoryRepository(ICategoryRepository):
    """A class implementing the category repository."""

    async def get_all_categories(self) -> Iterable[Any]:
        """The method getting all job categories from the data storage.

        Returns:
            Iterable[Any]: The collection of the all job categories.
        """

        query = category_table.select().order_by(category_table.c.name.asc())
        categories = await database.fetch_all(query)

        return [CategoryDTO.from_record(category) for category in categories]

    async def get_category_by_id(self, category_id: int) -> Any | None:
        """The method getting a job category from the data storage.

        Args:
            category_id (int): The id of the job category.

        Returns:
            Any | None: The job category data if exists.
        """

        category = await self._get_by_id(category_id)

        return CategoryDTO.form_record(category) if category else None

    async def get_category_by_offer(
        self,
        offer_id: int,
    ) -> Iterable[Any]:
        """The abstract getting provided offer's job category
            from the data storage.

        Args:
            offer_id (int): The id of the offer.

        Returns:
            Iterable[Any]: The collection of the job category.
        """

        query = (
            select(category_table, offer_table)
            .select_from(
                join(
                    category_table,
                    offer_table,
                    category_table.c.id == offer_table.c.category
                )
            ).where(offer_table.c.id == offer_id)
        )
        category = await database.fetch_one(query)

        return CategoryDTO.form_record(category) if category else None


    async def add_category(self, data: CategoryIn) -> Any | None:
        """The method adding new job category to the data storage.

        Args:
            data (CategoryIn): The attributes of the job category.

        Returns:
            Any | None: The newly created job category.
        """

        query = category_table.insert().values(**data.model_dump())
        new_category_id = await database.execute(query)
        new_category = await self._get_by_id(new_category_id)

        return Category(**dict(new_category)) if new_category else None

    async def update_category(
        self,
        category_id: int,
        data: CategoryIn,
    ) -> Any | None:
        """The method updating job category data in the data storage.

        Args:
            category_id (int): The job category id.
            data (CategoryIn): The attributes of the job category.

        Returns:
            Any | None: The updated job category.
        """

        if self._get_by_id(category_id):
            query = (
                category_table.update()
                .where(category_table.c.id == category_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            category = await self._get_by_id(category_id)

            return Category(**dict(category)) if category else None

        return None

    async def delete_category(self, category_id: int) -> bool:
        """The method updating removing job category from the data storage.

        Args:
            category_id (int): The job category id.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(category_id):
            query = category_table \
                .delete() \
                .where(category_table.c.id == category_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, category_id: int) -> Record | None:
        """A private method getting job category from the DB based on its ID.

        Args:
            category_id (int): The ID of the job category.

        Returns:
            Any | None: job category record if exists.
        """

        query = (
            category_table.select()
            .where(category_table.c.id == category_id)
            .order_by(category_table.c.name.asc())
        )

        return await database.fetch_one(query)