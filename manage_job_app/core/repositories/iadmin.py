""" Module containing admin repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from manage_job_app.core.domain.admin import AdminIn
from pydantic import UUID5


class IAdminRepository(ABC):
    """An abstract class representing protocol of admin repository."""

    @abstractmethod
    async def get_all_admins(self) -> Iterable[Any]:
        """The abstract getting all admins from the data storage.

        Returns:
            Iterable[Any]: The collection of the all admins.
        """

    @abstractmethod
    async def get_admin_by_id(self, admin_id: UUID5) -> Any | None:
        """The abstract getting an admin from the data storage.

        Args:
            admin_id (UUID5): The id of the admin.

        Returns:
            Any | None: The admin data if exists.
        """

    @abstractmethod
    async def get_admin_by_email(self, email: str) -> Any | None:
        """A method getting admin by email.

        Args:
            email (str): The email of the admin.

        Returns:
            Any | None: The admin object if exists.
        """

    @abstractmethod
    async def add_admin(self, data: AdminIn) -> Any | None:
        """The abstract adding new admin to the data storage.

        Args:
            data (AdminIn): The attributes of the admin.

        Returns:
            Any | None: The newly created admin.
        """

    @abstractmethod
    async def update_admin(
            self,
            admin_id: UUID5,
            data: AdminIn,
    ) -> Any | None:
        """The abstract updating admin data in the data storage.

        Args:
            admin_id (UUID5): The id of the admin.
            data (AdminIn): The details of the updated admin.

        Returns:
            Any | None: The updated admin details.
        """

    @abstractmethod
    async def delete_admin(self, admin_id: UUID5) -> bool:
        """The abstract updating removing admin from the data storage.

        Args:
            admin_id (UUID5): The id of the admin.

        Returns:
            bool: Success of the operation.
        """
