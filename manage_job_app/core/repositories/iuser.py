"""A repository for user entity."""

from abc import ABC, abstractmethod
from typing import Any, Iterable, Union

from pydantic import UUID5

from manage_job_app.core.domain.user import EmployerIn, EmployeeIn


class IUserRepository(ABC):
    """An abstract class representing protocol of user repository."""

    @abstractmethod
    async def get_all_users(self) -> Iterable[Any]:
        """The abstract getting all users from the data storage.

        Returns:
            Iterable[Any]: Users in the data storage.
        """

    @abstractmethod
    async def get_all_employers(self) -> Iterable[Any]:
        """The abstract getting all employers from the data storage.

            Returns:
                Iterable[Any]: Employers in the data storage.
        """

    @abstractmethod
    async def get_all_employees(self) -> Iterable[Any]:
        """The abstract getting all employees from the data storage.

            Returns:
                Iterable[Any]: Employees in the data storage.
        """


    @abstractmethod
    async def get_by_id(self, uuid: UUID5) -> Any | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID5): UUID of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def find_users_by_name(self, user_name: str) -> Iterable[Any]:
        """The abstract finding users by name.

        Args:
            user_name (str): The name to search for.

        Returns:
            Iterable[User]: Users matching the name.
        """


    @abstractmethod
    async def add_user(self, data: Union[EmployerIn, EmployeeIn]) -> Any | None:
        """The abstract adding new user to the data storage.

        Args:
            data (Union[EmployerIn, EmployeeIn]): The details of the new user.

        Returns:
            Any | None: The newly added user.
        """

    @abstractmethod
    async def update_user(
        self,
        user_id: UUID5,
        data: Union[EmployerIn, EmployeeIn],
    ) -> Any | None:
        """The abstract updating user data in the data storage.

        Args:
            user_id (UUID5): The id of the user.
            data (Union[EmployerIn, EmployeeIn]): The details of the updated user.

        Returns:
            User | None: The updated user details.
        """

    @abstractmethod
    async def delete_user(self, user_id: UUID5) -> bool:
        """The abstract updating removing user from the data storage.

        Args:
            user_id (UUID5): The id of the user.

        Returns:
            bool: Success of the operation.
        """
