"""Module containing application repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join, alias

from pydantic import UUID5

from manage_job_app.core.repositories.iapplication import IApplicationRepository
from manage_job_app.core.domain.application import Application, ApplicationBroker, ApplicationUpdateStatus
from manage_job_app.db import (
    application_table,
    offer_table,
    category_table,
    employer_table,
    employee_table,
    city_table,
    database,
)
from manage_job_app.infrastructure.dto.applicationdto import ApplicationDTO


class ApplicationRepository(IApplicationRepository):
    """A class representing application DB repository."""

    async def get_all_applications(self) -> Iterable[Any]:
        """The method getting all applications from the data storage.

        Returns:
            Iterable[Any]: Applications in the data storage.
        """

        city_author_alias = alias(city_table, name="cities_author")
        city_applicant_alias = alias(city_table, name="cities_applicant")
        city_offer_alias = alias(city_table, name="cities_offer")

        query = (
            select(application_table, offer_table, category_table, city_offer_alias, employer_table, employee_table, city_author_alias, city_applicant_alias)
            .select_from(
                join(
                    application_table,
                    offer_table,
                    application_table.c.offer_id == offer_table.c.id
                ).join(
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
                ).join(
                    employee_table,
                    application_table.c.user_id == employee_table.c.id
                ).join(
                    city_applicant_alias,
                    employee_table.c.city == city_applicant_alias.c.id
                )
            )
            .order_by(application_table.c.status.asc())
        )
        applications = await database.fetch_all(query)

        return [ApplicationDTO.from_record(application) for application in applications]


    async def get_by_id(self, application_id: int) -> Any | None:
        """The method getting application by provided id.

        Args:
            application_id (int): The id of the application.

        Returns:
            Any | None: The application details.
        """

        # user_author_alias = alias(user_table, name="users_author")
        # user_applicant_alias = alias(user_table, name="users_applicant")

        city_author_alias = alias(city_table, name="cities_author")
        city_applicant_alias = alias(city_table, name="cities_applicant")
        city_offer_alias = alias(city_table, name="cities_offer")

        query = (
            select(application_table, offer_table, category_table, city_offer_alias, employer_table, employee_table,
                   city_author_alias, city_applicant_alias)
            .select_from(
                join(
                    application_table,
                    offer_table,
                    application_table.c.offer_id == offer_table.c.id
                ).join(
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
                ).join(
                    employee_table,
                    application_table.c.user_id == employee_table.c.id
                ).join(
                    city_applicant_alias,
                    employee_table.c.city == city_applicant_alias.c.id
                )
            )
            .where(application_table.c.id == application_id)
            .order_by(application_table.c.status.asc())
        )

        application = await database.fetch_one(query)

        return ApplicationDTO.from_record(application) if application else None


    async def get_by_user(self, user_id: UUID5) -> Iterable[Any]:
        """The method getting applications by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: The application collection.
        """

        query = (
            select(application_table)
            .where(application_table.c.user_id == user_id)
            .order_by(application_table.c.status.asc())
        )

        applications = await database.fetch_all(query)

        return [dict(application) for application in applications]


    async def add_application(self, data: ApplicationBroker) -> Any | None:
        """The method adding new application to the data storage.

        Args:
            data (ApplicationBroker): The details of the new application.

        Returns:
            Application: Full details of the newly added application.

        Returns:
            Any | None: The newly added application.
        """

        query = application_table.insert().values(**data.model_dump())
        new_application_id = await database.execute(query)
        new_application = await self._get_by_id(new_application_id)

        return Application(**dict(new_application)) if new_application else None

    async def update_application(
        self,
        application_id: int,
        data: ApplicationBroker,
    ) -> Any | None:
        """The method updating application data in the data storage.

        Args:
            application_id (int): The id of the application.
            data (ApplicationBroker): The details of the updated application.

        Returns:
            Any | None: The updated application details.
        """

        if self._get_by_id(application_id):
            query = (
                application_table.update()
                .where(application_table.c.id == application_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            application = await self._get_by_id(application_id)

            return Application(**dict(application)) if application else None

        return None

    async def update_application_status(
        self,
        application_id: int,
        data: ApplicationUpdateStatus,
    ) -> Any | None:
        """The method updating application data in the data storage.

        Args:
            application_id (int): The id of the application.
            data (ApplicationBroker): The details of the updated application.

        Returns:
            Any | None: The updated application details.
        """

        if self._get_by_id(application_id):
            query = (
                application_table.update()
                .where(application_table.c.id == application_id)
                .values(status=data.status)
            )
            await database.execute(query)

            application = await self._get_by_id(application_id)

            return Application(**dict(application)) if application else None

        return None

    async def delete_application(self, application_id: int) -> bool:
        """The method updating removing application from the data storage.

        Args:
            application_id (int): The id of the application.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(application_id):
            query = application_table \
                .delete() \
                .where(application_table.c.id == application_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, application_id: int) -> Record | None:
        """A private method getting application from the DB based on its ID.

        Args:
            application_id (int): The ID of the application.

        Returns:
            Any | None: Offer record if exists.
        """

        query = (
            application_table.select()
            .where(application_table.c.id == application_id)
            .order_by(application_table.c.status.asc())
        )

        return await database.fetch_one(query)