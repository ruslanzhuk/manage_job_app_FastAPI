"""Module containing admin service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID5

from manage_job_app.core.domain.admin import Admin, AdminIn
from manage_job_app.infrastructure.dto.admindto import AdminDTO
from manage_job_app.infrastructure.dto.tokendto import TokenDTO


class IAdminService(ABC):
    """An abstract class representing protocol of admin repository."""

    @abstractmethod
    async def get_all_admins(self) -> Iterable[AdminDTO]:
        """The abstract getting all admins from the repository.

        Returns:
            Iterable[AdminDTO]: The collection of the all admins.
        """

    @abstractmethod
    async def get_admin_by_id(self, admin_id: UUID5) -> AdminDTO | None:
        """The abstract getting an admin from the repository.

        Args:
            admin_id (UUID5): The id of the admin.

        Returns:
            AdminDTO | None: The admin data if exists.
        """

    @abstractmethod
    async def get_admin_by_email(self, email: str) -> AdminDTO | None:
        """A method getting admin by email.

        Args:
            email (str): The email of the admin.

        Returns:
            AdminDTO | None: The admin data, if found.
        """

    @abstractmethod
    async def add_admin(self, data: AdminIn) -> Admin | None:
        """The abstract adding new admin to the repository.

        Args:
            data (AdminIn): The attributes of the admin.

        Returns:
            Admin | None: The newly created admin.
        """

    @abstractmethod
    async def authenticate_admin(self, data: AdminIn) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            data (AdminIn): The user data.

        Returns:
            TokenDTO | None: The token details.
        """

    @abstractmethod
    async def update_admin(
        self,
        admin_id: UUID5,
        data: AdminIn,
    ) -> Admin | None:
        """The abstract updating admin data in the repository.

        Args:
            admin_id (UUID5): The admin id.
            data (AdminIn): The attributes of the admin.

        Returns:
            Admin | None: The updated admin.
        """

    @abstractmethod
    async def delete_admin(self, admin_id: UUID5) -> bool:
        """The abstract updating removing admin from the repository.

        Args:
            admin_id (UUID5): The admin id.

        Returns:
            bool: Success of the operation.
        """