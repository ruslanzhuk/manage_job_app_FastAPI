"""Module containing admin repository implementation."""
from datetime import datetime
from typing import Any, Iterable, Union

from pydantic import UUID5

from manage_job_app.infrastructure.dto.admindto import AdminDTO
from manage_job_app.infrastructure.utils.password import hash_password

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join, func

from manage_job_app.core.repositories.iadmin import IAdminRepository
from manage_job_app.core.domain.admin import AdminIn, Admin
from manage_job_app.db import (
    admin_table,
    database,
)


class AdminRepository(IAdminRepository):
    """A class representing admin DB repository."""

    async def get_all_admins(self) -> Iterable[Any]:
        """The method getting all admins from the data storage.

        Returns:
            Iterable[Any]: Admins in the data storage.
        """


        query = admin_table.select()

        admins = await database.fetch_all(query)


        return ([AdminDTO.from_record(admin) for admin in admins])


    async def get_admin_by_id(self, admin_id: UUID5) -> Any | None:
        """The method getting admin by provided id.

        Args:
            admin_id (UUID5): The id of the admin.

        Returns:
            Any | None: The admin details.
        """
        admin = await self._get_by_id(admin_id)

        return AdminDTO.from_record(admin) if admin else None

    async def get_admin_by_email(self, email: str) -> Any | None:
        """A method getting admin by email.

        Args:
            email (str): The email of the admin.

        Returns:
            Any | None: The admin object if exists.
        """

        query = select(admin_table).where(admin_table.c.email == email)

        admin = await database.fetch_one(query)
        if admin:
            return admin

        return None



    async def add_admin(self, data: AdminIn) -> Any | None:
        """The method adding new admin to the data storage.

        Args:
            data (AdminIn): The details of the new admin.

        Returns:
            Any | None: The newly added admin.
        """

        data.password = hash_password(data.password)


        query = admin_table.insert().values(**data.model_dump())
        new_admin_id = await database.execute(query)
        new_admin = await self._get_by_id(new_admin_id)

        return Admin(**dict(new_admin)) if new_admin else None


    async def update_admin(
        self,
        admin_id: UUID5,
        data: AdminIn,
    ) -> Any | None:
        """The method updating admin data in the data storage.

        Args:
            admin_id (UUID5): The id of the admin.
            data (AdminIn): The details of the updated admin.

        Returns:
            Any | None: The updated admin details.
        """


        query_custom = select(admin_table).where(admin_table.c.id == admin_id)
        admin_custom = await database.fetch_one(query_custom)

        data.password = hash_password(data.password)

        if await self._get_by_id(admin_id):
            update_data = {
                **data.model_dump(),
                "created_at": admin_custom["created_at"],
                "updated_at": datetime.now()
            }

            query = (
                admin_table.update()
                .where(admin_table.c.id == admin_id)
                .values(**update_data)
            )
            await database.execute(query)

            admin = await self._get_by_id(admin_id)

            return Admin(**dict(admin)) if admin else None

        return None


    async def delete_admin(self, admin_id: UUID5) -> bool:
        """The method removing a admin from the data storage.

        Args:
            admin_id (UUID5): The id of the admin.

        Returns:
            bool: Success of the operation.
        """

        admin = await self._get_by_id(admin_id)
        if not admin:
            return False

        query = admin_table \
            .delete() \
            .where(admin_table.c.id == admin_id)
        await database.execute(query)

        return True

    async def _get_by_id(self, admin_id: UUID5) -> Record | None:
        """A private method getting admin from the DB based on its ID.

        Args:
            admin_id (UUID5): The ID of the admin.

        Returns:
            Any | None: admin record if exists.
        """

        query = (
            admin_table.select()
            .where(admin_table.c.id == admin_id)
        )
        admin = await database.fetch_one(query)
        if admin:
            return admin

        return None
