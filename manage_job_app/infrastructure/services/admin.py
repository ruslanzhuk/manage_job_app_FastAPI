"""Module containing admin service implementation."""

from typing import Iterable, Union

from pydantic import UUID4

from manage_job_app.core.domain.admin import AdminIn, Admin
from manage_job_app.core.repositories.iadmin import IAdminRepository
from manage_job_app.infrastructure.dto.admindto import AdminDTO
from manage_job_app.infrastructure.services.iadmin import IAdminService
from manage_job_app.infrastructure.dto.tokendto import TokenDTO
from manage_job_app.infrastructure.utils.password import verify_password
from manage_job_app.infrastructure.utils.token import generate_admin_token

class AdminService(IAdminService):
    """A class implementing the admin service."""

    _repository: IAdminRepository

    def __init__(self, repository: IAdminRepository) -> None:
        """The initializer of the `admin service`.

        Args:
            repository (IAdminRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all_admins(self) -> Iterable[AdminDTO]:
        """The method getting all admins from the repository.

        Returns:
            Iterable[AdminDTO]: All admins.
        """

        return await self._repository.get_all_admins()


    async def get_admin_by_id(self, admin_id: UUID4) -> AdminDTO | None:
        """The method getting admin by provided id.

        Args:
            admin_id (UUID4): The id of the admin.

        Returns:
            AdminDTO | None: The admin details.
        """

        return await self._repository.get_admin_by_id(admin_id)

    async def get_admin_by_email(self, email: str) -> AdminDTO | None:
        """A method getting admin by email.

        Args:
            email (str): The email of the admin.

        Returns:
            AdminDTO | None: The admin data, if found.
        """

        return await self._repository.get_admin_by_email(email)


    async def add_admin(self, data: AdminIn) -> Admin | None:
        """The method adding new admin to the data storage.

        Args:
            data (AdminIn): The details of the new admin.

        Returns:
            Admin | None: The newly added admin.
        """

        return await self._repository.add_admin(data)

    async def authenticate_admin(self, data: AdminIn) -> TokenDTO | None:
        """The method authenticating the admin.

        Args:
            data (AdminIn): The admin data.

        Returns:
            TokenDTO | None: The token details.
        """

        if admin_data := await self._repository.get_admin_by_email(data.email):
            if verify_password(data.password, admin_data.password):
                token_details = generate_admin_token(admin_data.id)
                # trunk-ignore(bandit/B106)
                return TokenDTO(token_type="Bearer", **token_details)

            return None

        return None

    async def update_admin(self, admin_id: UUID4, data: AdminIn) -> Admin | None:
        """The method updating admin data in the data storage.

        Args:
            admin_id (UUID4): The id of the admin.
            data (AdminIn): The details of the updated admin.

        Returns:
            Admin | None: The updated admin details.
        """

        return await self._repository.update_admin(admin_id=admin_id, data=data)

    async def delete_admin(self, admin_id: UUID4) -> bool:
        """The method removing an admin from the data storage.

        Args:
            admin_id (UUID4): The id of the admin.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_admin(admin_id)