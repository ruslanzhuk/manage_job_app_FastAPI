"""Module containing user repository implementation."""
from datetime import datetime
from typing import Any, Iterable, Union

from pydantic import UUID5

from manage_job_app.infrastructure.utils.password import hash_password

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join, func

from manage_job_app.core.repositories.iuser import IUserRepository
from manage_job_app.core.domain.user import EmployerIn, EmployeeIn, Employer, Employee, UserIn
from manage_job_app.db import (
    employer_table,
    employee_table,
    city_table,
    database,
)
from manage_job_app.infrastructure.dto.userdto import EmployerDTO, EmployeeDTO


class UserRepository(IUserRepository):
    """A class representing user DB repository."""

    async def get_all_users(self) -> Iterable[Any]:
        """The method getting all users from the data storage.

        Returns:
            Iterable[Any]: Users in the data storage.
        """

        columns_to_select = [
            column for column in employer_table.c if column.name != "password"
        ]

        query = (
            select(*columns_to_select, city_table)
            .select_from(
                join(
                    employer_table,
                    city_table,
                    employer_table.c.city == city_table.c.id,
                    isouter=True
                )
            )
            .order_by(employer_table.c.name.asc())
        )

        employers = await database.fetch_all(query)

        columns_to_select = [
            column for column in employee_table.c if column.name != "password"
        ]

        query = (
            select(*columns_to_select, city_table)
            .select_from(
                join(
                    employee_table,
                    city_table,
                    employee_table.c.city == city_table.c.id,
                    isouter=True
                )
            )
            .order_by(employee_table.c.name.asc())
        )

        employees = await database.fetch_all(query)



        return ([EmployerDTO.from_record(employer) for employer in employers]
                + [EmployeeDTO.from_record(employee) for employee in employees])

    async def get_all_employers(self) -> Iterable[Any]:
        """The method getting all employers from the data storage.

            Returns:
                Iterable[Any]: Employers in the data storage.
        """

        columns_to_select = [
            column for column in employer_table.c if column.name != "password"
        ]

        query = (
            select(*columns_to_select, city_table)
            .select_from(
                join(
                    employer_table,
                    city_table,
                    employer_table.c.city == city_table.c.id,
                    isouter=True
                )
            )
            .order_by(employer_table.c.name.asc())
        )

        employers = await database.fetch_all(query)

        return ([EmployerDTO.from_record(employer) for employer in employers])

    async def get_all_employees(self) -> Iterable[Any]:
        """The method getting all employees from the data storage.

            Returns:
                Iterable[Any]: Employees in the data storage.
        """

        columns_to_select = [
            column for column in employee_table.c if column.name != "password"
        ]

        query = (
            select(*columns_to_select, city_table)
            .select_from(
                join(
                    employee_table,
                    city_table,
                    employee_table.c.city == city_table.c.id,
                    isouter=True
                )
            )
            .order_by(employee_table.c.name.asc())
        )

        employees = await database.fetch_all(query)

        return ([EmployeeDTO.from_record(employee) for employee in employees])


    async def get_by_id(self, user_id: UUID5) -> Any | None:
        """The method getting user by provided id.

        Args:
            user_id (UUID5): The id of the user.

        Returns:
            Any | None: The user details.
        """
        employer_query = (
            select(employer_table, city_table)
            .select_from(
                join(
                    employer_table,
                    city_table,
                    employer_table.c.city == city_table.c.id,
                    isouter=True
                )
            ).where(employer_table.c.id == user_id))
        employee_query = (
            select(employee_table, city_table)
            .select_from(
                join(
                    employee_table,
                    city_table,
                    employee_table.c.city == city_table.c.id,
                    isouter=True
                )
            ).where(employee_table.c.id == user_id))

        employer = await database.fetch_one(employer_query)
        if employer:
            return EmployerDTO.from_record(employer)

        employee = await database.fetch_one(employee_query)
        if employee:
            return EmployeeDTO.from_record(employee)

        return None

    async def get_by_email(self, email: str) -> Any | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if exists.
        """

        employer_query = select(employer_table).where(employer_table.c.email == email)
        employee_query = select(employee_table).where(employee_table.c.email == email)

        employer = await database.fetch_one(employer_query)
        if employer:
            return employer

        employee = await database.fetch_one(employee_query)
        if employee:
            return employee

        return None

    async def find_users_by_name(self, user_name: str) -> Iterable[Any]:
        """The method to find users by name.

        Args:
            user_name (str): The name or part of the name to search for.

        Returns:
            Iterable[Any]: A list of users matching the name criteria.
        """

        columns_to_select = [
            column for column in employer_table.c if column.name != "password"
        ]

        employer_query = (
            select(*columns_to_select, city_table)
            .select_from(
                join(
                    employer_table,
                    city_table,
                    employer_table.c.city == city_table.c.id,
                    isouter=True
                )
            ).where(func.lower(employer_table.c.name).like(f"%{user_name.lower()}%"))
            .order_by(employer_table.c.name.asc())
        )

        columns_to_select = [
            column for column in employer_table.c if column.name != "password"
        ]

        employee_query = (
            select(*columns_to_select, city_table)
            .select_from(
                join(
                    employee_table,
                    city_table,
                    employee_table.c.city == city_table.c.id,
                    isouter=True
                )
            ).where(func.lower(employee_table.c.name).like(f"%{user_name.lower()}%"))
            .order_by(employee_table.c.name.asc())
        )

        employers = await database.fetch_all(employer_query)
        employees = await database.fetch_all(employee_query)

        return [
            EmployerDTO.from_record(employer) for employer in employers
        ] + [
            EmployeeDTO.from_record(employee) for employee in employees
        ]


    async def add_user(self, data: Union[EmployerIn, EmployeeIn]) -> Any | None:
        """The method adding new user to the data storage.

        Args:
            data (Union[EmployerIn, EmployeeIn]): The details of the new user.

        Returns:
            Any | None: The newly added user.
        """

        data.password = hash_password(data.password)

        if isinstance(data, EmployerIn):
            table = employer_table
            result_model = Employer
        elif isinstance(data, EmployeeIn):
            table = employee_table
            result_model = Employee

        query = table.insert().values(**data.model_dump())
        new_user_id = await database.execute(query)
        new_user = await self._get_by_id(new_user_id)

        return result_model(**dict(new_user)) if new_user else None


    async def update_user(
        self,
        user_id: UUID5,
        data: Union[EmployerIn, EmployeeIn],
    ) -> Any | None:
        """The method updating user data in the data storage.

        Args:
            user_id (UUID5): The id of the user.
            data (Union[EmployerIn, EmployeeIn]): The details of the updated user.

        Returns:
            Any | None: The updated user details.
        """

        if isinstance(data, EmployerIn):
            table = employer_table
            result_model = Employer
        elif isinstance(data, EmployeeIn):
            table = employee_table
            result_model = Employee

        print("Początek")
        print(table)
        print(result_model)

        query_custom = select(table).where(table.c.id == user_id)
        user_custom = await database.fetch_one(query_custom)
        print(user_custom["created_at"])
        data.password = hash_password(data.password)

        if await self._get_by_id(user_id):
            update_data = {
                **data.model_dump(),
                "created_at": user_custom["created_at"],
                "updated_at": datetime.now()
            }

            query = (
                table.update()
                .where(table.c.id == user_id)
                .values(**update_data)
            )
            await database.execute(query)

            user = await self._get_by_id(user_id)

            return result_model(**dict(user)) if user else None

        return None


    async def delete_user(self, user_id: UUID5) -> bool:
        """The method removing a user from the data storage.

        Args:
            user_id (UUID5): The id of the user.

        Returns:
            bool: Success of the operation.
        """

        user = await self._get_by_id(user_id)
        if not user:
            return False

        if "company_name" in user:
            table = employer_table
        elif "skills" in user:
            table = employee_table

        query = table \
            .delete() \
            .where(table.c.id == user_id)
        await database.execute(query)

        return True

    async def _get_by_id(self, user_id: UUID5) -> Record | None:
        """A private method getting user from the DB based on its ID.

        Args:
            user_id (UUID5): The ID of the user.

        Returns:
            Any | None: User record if exists.
        """

        query_employer = (
            employer_table.select()
            .where(employer_table.c.id == user_id)
        )
        employer = await database.fetch_one(query_employer)
        if employer:
            return employer

        query_employee = (
            employee_table.select()
            .where(employee_table.c.id == user_id)
        )
        employee = await database.fetch_one(query_employee)
        if employee:
            return employee