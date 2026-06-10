"""Module containing review repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join, alias

from pydantic import UUID5

from manage_job_app.core.repositories.ireview import IReviewRepository
from manage_job_app.core.domain.review import Review, ReviewBroker, ReviewUpdateStatus
from manage_job_app.db import (
    review_table,
    employer_table,
    employee_table,
    city_table,
    database,
)
from manage_job_app.infrastructure.dto.reviewdto import ReviewDTO


class ReviewRepository(IReviewRepository):
    """A class representing review DB repository."""

    async def get_all_reviews(self) -> Iterable[Any]:
        """The method getting all reviews from the data storage.

        Returns:
            Iterable[Any]: Reviews in the data storage.
        """

        # user_employee_alias = alias(user_table, name="users_employee")
        # user_employer_alias = alias(user_table, name="users_employer")
        city_employer_alias = alias(city_table, name="cities_employer")
        city_employee_alias = alias(city_table, name="cities_employee")

        query = (
            select(review_table, employee_table, employer_table, city_employer_alias, city_employee_alias)
            .select_from(
                join(
                    review_table,
                    employee_table,
                    review_table.c.employee_id == employee_table.c.id
                ).join(
                    city_employee_alias,
                    employee_table.c.city == city_employee_alias.c.id
                ).join(
                    employer_table,
                    review_table.c.employer_id == employer_table.c.id
                ).join(
                    city_employer_alias,
                    employer_table.c.city == city_employer_alias.c.id
                )
            )
        )
        reviews = await database.fetch_all(query)

        return [ReviewDTO.from_record(review) for review in reviews]


    async def get_by_id(self, review_id: int) -> Any | None:
        """The method getting review by provided id.

        Args:
            review_id (int): The id of the review.

        Returns:
            Any | None: The review details.
        """

        # user_employee_alias = alias(user_table, name="users_employee")
        # user_employer_alias = alias(user_table, name="users_employer")
        city_employer_alias = alias(city_table, name="cities_employer")
        city_employee_alias = alias(city_table, name="cities_employee")

        query = (
            select(review_table, employee_table, employer_table, city_employer_alias, city_employee_alias)
            .select_from(
                join(
                    review_table,
                    employee_table,
                    review_table.c.employee_id == employee_table.c.id
                ).join(
                    city_employee_alias,
                    employee_table.c.city == city_employee_alias.c.id
                ).join(
                    employer_table,
                    review_table.c.employer_id == employer_table.c.id
                ).join(
                    city_employer_alias,
                    employer_table.c.city == city_employer_alias.c.id
                )
            )
            .where(review_table.c.id == review_id)
        )

        review = await database.fetch_one(query)

        return ReviewDTO.from_record(review) if review else None


    async def get_by_user(self, user_id: UUID5) -> Iterable[Any]:
        """The method getting reviews by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: The review collection.
        """

        query = (
            select(review_table)
            .where(review_table.c.employer_id == user_id)
        )

        reviews = await database.fetch_all(query)

        return [dict(review) for review in reviews]

    async def get_by_user_belongs(self, employee_id: UUID5) -> Iterable[Any]:
        """The method getting reviews by user who own.

        Args:
            employee_id (UUID5): The id of the user who own the review.

        Returns:
            Iterable[Any]: The review collection.
        """

        query = (
            select(review_table)
            .where(review_table.c.employee_id == employee_id)
        )

        reviews = await database.fetch_all(query)

        return [dict(review) for review in reviews]

    async def add_review(self, data: ReviewBroker) -> Any | None:
        """The method adding new review to the data storage.

        Args:
            data (ReviewBroker): The details of the new review.

        Returns:
            Review: Full details of the newly added review.

        Returns:
            Any | None: The newly added review.
        """

        query = review_table.insert().values(**data.model_dump())
        new_review_id = await database.execute(query)
        new_review = await self._get_by_id(new_review_id)

        return Review(**dict(new_review)) if new_review else None

    async def update_review(
        self,
        review_id: int,
        data: ReviewBroker,
    ) -> Any | None:
        """The method updating review data in the data storage.

        Args:
            review_id (int): The id of the review.
            data (ReviewIn): The details of the updated review.

        Returns:
            Any | None: The updated review details.
        """

        if self._get_by_id(review_id):
            query = (
                review_table.update()
                .where(review_table.c.id == review_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            review = await self._get_by_id(review_id)

            return Review(**dict(review)) if review else None

        return None

    async def update_review_status(
        self,
        review_id: int,
        data: ReviewUpdateStatus,
    ) -> Any | None:
        """The method updating review status in the data storage.

        Args:
            review_id (int): The id of the review.
            data (ReviewIn): The details of the updated review.

        Returns:
            Any | None: The updated review details.
        """

        if self._get_by_id(review_id):
            query = (
                review_table.update()
                .where(review_table.c.id == review_id)
                .values(status=data.status)
            )
            await database.execute(query)

            review = await self._get_by_id(review_id)

            return Review(**dict(review)) if review else None

        return None

    async def delete_review(self, review_id: int) -> bool:
        """The method updating removing review from the data storage.

        Args:
            review_id (int): The id of the review.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(review_id):
            query = review_table \
                .delete() \
                .where(review_table.c.id == review_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, review_id: int) -> Record | None:
        """A private method getting review from the DB based on its ID.

        Args:
            review_id (int): The ID of the review.

        Returns:
            Any | None: Review record if exists.
        """

        query = (
            review_table.select()
            .where(review_table.c.id == review_id)
        )

        return await database.fetch_one(query)