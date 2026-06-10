"""Module containing job category service implementation."""

from typing import Iterable


from manage_job_app.core.domain.job_category import Category, CategoryIn
from manage_job_app.core.repositories.ijob_category import ICategoryRepository
from manage_job_app.infrastructure.dto.job_categorydto import CategoryDTO
from manage_job_app.infrastructure.services.ijob_category import ICategoryService


class CategoryService(ICategoryService):
    """A class implementing the job category service."""

    _repository: ICategoryRepository

    def __init__(self, repository: ICategoryRepository) -> None:
        """The initializer of the `job category service`.

        Args:
            repository (ICategoryRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all_categories(self) -> Iterable[CategoryDTO]:
        """The method getting all job categories from the repository.

        Returns:
            Iterable[CategoryDTO]: The collection of the all job categories.
        """

        return await self._repository.get_all_categories()

    async def get_category_by_id(self, category_id: int) -> CategoryDTO | None:
        """The method getting a job category from the repository.

        Args:
            category_id (int): The id of the job category.

        Returns:
            CategoryDTO | None: The job category data if exists.
        """

        return await self._repository.get_category_by_id(category_id)

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

        return await self._repository.get_category_by_offer(offer_id)


    async def add_category(self, data: CategoryIn) -> Category | None:
        """The method adding new job category to the repository.

        Args:
            data (categoryIn): The attributes of the job category.

        Returns:
            Category | None: The newly created job category.
        """

        return await self._repository.add_category(data)

    async def update_category(
        self,
        category_id: int,
        data: CategoryIn,
    ) -> Category | None:
        """The method updating job category data in the repository.

        Args:
            category_id (int): The job category id.
            data (categoryIn): The attributes of the job category.

        Returns:
            Category | None: The updated job category.
        """

        return await self._repository.update_category(
            category_id=category_id,
            data=data,
        )

    async def delete_category(self, category_id: int) -> bool:
        """The method updating removing job category from the repository.

        Args:
            category_id (int): The job category id.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_category(category_id)