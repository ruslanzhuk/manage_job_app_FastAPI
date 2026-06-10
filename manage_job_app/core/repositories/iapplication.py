"""Module containing application repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from manage_job_app.core.domain.application import ApplicationBroker, ApplicationUpdateStatus

from pydantic import UUID5


class IApplicationRepository(ABC):
    """An abstract class representing protocol of application repository."""

    @abstractmethod
    async def get_all_applications(self) -> Iterable[Any]:
        """The abstract getting all applications from the data storage.

        Returns:
            Iterable[Application]: Applications in the data storage.
        """


    @abstractmethod
    async def get_by_id(self, application_id: int) -> Any | None:
        """The abstract getting application by provided id.

        Args:
            application_id (int): The id of the application.

        Returns:
            Application | None: The application details.
        """



    @abstractmethod
    async def get_by_user(self, user_id: UUID5) -> Iterable[Any]:
        """The abstract getting applications by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Application]: The application collection.
        """


    @abstractmethod
    async def add_application(self, data: ApplicationBroker) -> Any | None:
        """The abstract adding new application to the data storage.

        Args:
            data (ApplicationIn): The details of the new application.

        Returns:
            Any | None: The newly added application.
        """

    @abstractmethod
    async def update_application(
        self,
        application_id: int,
        data: ApplicationBroker,
    ) -> Any | None:
        """The abstract updating application data in the data storage.

        Args:
            application_id (int): The id of the offer.
            data (ApplicationIn): The details of the updated application.

        Returns:
            Application | None: The updated application details.
        """

    @abstractmethod
    async def update_application_status(
        self,
        application_id: int,
        data: ApplicationUpdateStatus,
    ) -> Any | None:
        """The abstract updating application status in the data storage.

        Args:
            application_id (int): The id of the offer.
            data (ApplicationIn): The details of the updated application.

        Returns:
            Application | None: The updated application details.
        """

    @abstractmethod
    async def delete_application(self, application_id: int) -> bool:
        """The abstract updating removing application from the data storage.

        Args:
            application_id (int): The id of the application.

        Returns:
            bool: Success of the operation.
        """