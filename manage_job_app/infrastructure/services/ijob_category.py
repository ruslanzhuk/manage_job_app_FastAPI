"""Module containing job category service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from manage_job_app.core.domain.job_category import Category, CategoryIn
from manage_job_app.infrastructure.dto.job_categorydto import CategoryDTO


class ICategoryService(ABC):
    """An abstract class representing protocol of job category repository."""

    @abstractmethod
    async def get_all_categories(self) -> Iterable[CategoryDTO]:
        """The abstract getting all job categories from the repository.

        Returns:
            Iterable[category]: The collection of the all job categories.
        """

    @abstractmethod
    async def get_category_by_id(self, category_id: int) -> CategoryDTO | None:
        """The abstract getting a job category from the repository.

        Args:
            category_id (int): The id of the job category.

        Returns:
            category | None: The job category data if exists.
        """

    @abstractmethod
    async def get_category_by_offer(
            self,
            offer_id: int,
    ) -> CategoryDTO | None:
        """The abstract getting provided offer's job category
            from the repository.

        Args:
            offer_id (int): The id of the offer.

        Returns:
            CategoryDTO | None: The job category data if exists.
        """

    @abstractmethod
    async def add_category(self, data: CategoryIn) -> Category | None:
        """The abstract adding new job category to the repository.

        Args:
            data (categoryIn): The attributes of the job category.

        Returns:
            Category | None: The newly created job category.
        """

    @abstractmethod
    async def update_category(
        self,
        category_id: int,
        data: CategoryIn,
    ) -> Category | None:
        """The abstract updating job category data in the repository.

        Args:
            category_id (int): The job category id.
            data (categoryIn): The attributes of the job category.

        Returns:
            Category | None: The updated job category.
        """

    @abstractmethod
    async def delete_category(self, category_id: int) -> bool:
        """The abstract updating removing job category from the repository.

        Args:
            category_id (int): The job category id.

        Returns:
            bool: Success of the operation.
        """