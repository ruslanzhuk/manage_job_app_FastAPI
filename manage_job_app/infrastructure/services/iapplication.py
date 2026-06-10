"""Module containing application service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from manage_job_app.core.domain.application import Application, ApplicationBroker, ApplicationUpdateStatus
from manage_job_app.infrastructure.dto.applicationdto import ApplicationDTO

from pydantic import UUID5


class IApplicationService(ABC):
    """A abstract class providing the Application service."""

    @abstractmethod
    async def get_all(self) -> Iterable[ApplicationDTO]:
        """The method getting all applications from the repository.

        Returns:
            Iterable[ApplicationDTO]: All applications.
        """

    @abstractmethod
    async def get_by_id(self, application_id: int) -> ApplicationDTO | None:
        """The method getting an application by provided id.

        Args:
            application_id (int): The ID of the application.

        Returns:
            ApplicationDTO | None: The application details.
        """

    @abstractmethod
    async def get_by_user(self, user_id: UUID5) -> Iterable[Application]:
        """The method getting applications by user who added them.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Iterable[Application]: The application collection.
        """


    @abstractmethod
    async def add_application(self, data: ApplicationBroker) -> Application | None:
        """The method adding new application to the data storage.

        Args:
            data (ApplicationIn): The data of the new application.

        Returns:
            Application | None: Full details of the newly added application.
        """

    @abstractmethod
    async def update_application(self, application_id: int, data: ApplicationBroker) -> Application | None:
        """The method updating application data in the data storage.

        Args:
            application_id (int): The ID of the application.
            data (ApplicationIn): The new data for the application.

        Returns:
            Application | None: The updated application details.
        """

    @abstractmethod
    async def update_application_status(self, application_id: int, data: ApplicationUpdateStatus) -> Application | None:
        """The method updating application status in the data storage.

        Args:
            application_id (int): The ID of the application.
            data (ApplicationIn): The new data for the application.

        Returns:
            Application | None: The updated application details.
        """

    @abstractmethod
    async def delete_application(self, application_id: int) -> bool:
        """The method updating removing application from the data storage.

        Args:
            application_id (int): The ID of the application.

        Returns:
            bool: Success of the operation.
        """