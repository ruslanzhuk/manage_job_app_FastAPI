"""Module containing application service implementation."""

from typing import Iterable

from manage_job_app.core.domain.application import Application, ApplicationBroker, ApplicationUpdateStatus
from manage_job_app.core.repositories.iapplication import IApplicationRepository
from manage_job_app.infrastructure.dto.applicationdto import ApplicationDTO
from manage_job_app.infrastructure.services.iapplication import IApplicationService

from pydantic import UUID5


class ApplicationService(IApplicationService):
    """A class implementing the offer service."""

    _repository: IApplicationRepository

    def __init__(self, repository: IApplicationRepository) -> None:
        """The initializer of the `application service`.

        Args:
            repository (IApplicationRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[ApplicationDTO]:
        """The method getting all applications from the repository.

        Returns:
            Iterable[ApplicationDTO]: All applications.
        """

        return await self._repository.get_all_applications()


    async def get_by_id(self, application_id: int) -> ApplicationDTO | None:
        """The method getting application by provided id.

        Args:
            application_id (int): The id of the application.

        Returns:
            ApplicationDTO | None: The application details.
        """

        return await self._repository.get_by_id(application_id)


    async def get_by_user(self, user_id: UUID5) -> Iterable[Application]:
        """The method getting applications by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Application]: The application collection.
        """

        return await self._repository.get_by_user(user_id)


    async def add_application(self, data: ApplicationBroker) -> Application | None:
        """The method adding new application to the data storage.

        Args:
            data (ApplicationIn): The details of the new application.

        Returns:
            Application | None: Full details of the newly added application.
        """

        return await self._repository.add_application(data)

    async def update_application(
        self,
        application_id: int,
        data: ApplicationBroker,
    ) -> Application | None:
        """The method updating application data in the data storage.

        Args:
            application_id (int): The id of the application.
            data (ApplicationIn): The details of the updated application.

        Returns:
            Application | None: The updated application details.
        """

        return await self._repository.update_application(
            application_id=application_id,
            data=data,
        )

    async def update_application_status(
            self,
            application_id: int,
            data: ApplicationUpdateStatus
    ) -> Application | None:
        """The method updating application status in the data storage.

        Args:
            application_id (int): The id of the application.
            data (ApplicationIn): The details of the updated application.

        Returns:
            Application | None: The updated application details.
        """

        return await self._repository.update_application_status(
            application_id=application_id,
            data=data,
        )

    async def delete_application(self, application_id: int) -> bool:
        """The method updating removing application from the data storage.

        Args:
            application_id (int): The id of the application.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_application(application_id)