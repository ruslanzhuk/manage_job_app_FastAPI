""" Module containing job category repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from manage_job_app.core.domain.job_category import CategoryIn


class ICategoryRepository(ABC):
    """An abstract class representing protocol of job category repository."""

    @abstractmethod
    async def get_all_categories(self) -> Iterable[Any]:
        """The abstract getting all job categories from the data storage.

        Returns:
            Iterable[Any]: The collection of the all job categories.
        """

    @abstractmethod
    async def get_category_by_id(self, category_id: int) -> Any | None:
        """The abstract getting a job category from the data storage.

        Args:
            category_id (int): The id of the job category.

        Returns:
            Any | None: The job category data if exists.
        """

    @abstractmethod
    async def get_category_by_offer(
            self,
            offer_id: int,
    ) -> Any | None:
        """The abstract getting provided offer's job category
            from the data storage.

        Args:
            offer_id (int): The id of the offer.

        Returns:
            Any | None: The job category data if exists.
        """

    @abstractmethod
    async def add_category(self, data: CategoryIn) -> Any | None:
        """The abstract adding new job category to the data storage.

        Args:
            data (CategoryIn): The attributes of the job category.

        Returns:
            Any | None: The newly created job category.
        """

    @abstractmethod
    async def update_category(
            self,
            category_id: int,
            data: CategoryIn,
    ) -> Any | None:
        """The abstract updating job category data in the data storage.

        Args:
            category_id (int): The id of the job category.
            data (CategoryIn): The details of the updated job category.

        Returns:
            Any | None: The updated job category details.
        """

    @abstractmethod
    async def delete_category(self, category_id: int) -> bool:
        """The abstract updating removing job category from the data storage.

        Args:
            category_id (int): The id of the job category.

        Returns:
            bool: Success of the operation.
        """