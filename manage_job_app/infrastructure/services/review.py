"""Module containing review service implementation."""

from typing import Iterable

from manage_job_app.core.domain.review import Review, ReviewBroker, ReviewUpdateStatus
from manage_job_app.core.repositories.ireview import IReviewRepository
from manage_job_app.infrastructure.dto.reviewdto import ReviewDTO
from manage_job_app.infrastructure.services.ireview import IReviewService

from pydantic import UUID5


class ReviewService(IReviewService):
    """A class implementing the review service."""

    _repository: IReviewRepository

    def __init__(self, repository: IReviewRepository) -> None:
        """The initializer of the `review service`.

        Args:
            repository (IReviewRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[ReviewDTO]:
        """The method getting all reviews from the repository.

        Returns:
            Iterable[ReviewDTO]: All reviews.
        """

        return await self._repository.get_all_reviews()


    async def get_by_id(self, review_id: int) -> ReviewDTO | None:
        """The method getting review by provided id.

        Args:
            review_id (int): The id of the review.

        Returns:
            ReviewDTO | None: The review details.
        """

        return await self._repository.get_by_id(review_id)


    async def get_by_user(self, user_id: UUID5) -> Iterable[Review]:
        """The method getting reviews by user who added them.

        Args:
            user_id (UUID5): The id of the user.

        Returns:
            Iterable[Review]: The review collection.
        """

        return await self._repository.get_by_user(user_id)

    async def get_by_user_belongs(self, employee_id: UUID5) -> Iterable[Review]:
        """The method getting reviews by user who own.

        Args:
            employee_id (UUID5): The id of the user.

        Returns:
            Iterable[Review]: The review collection.
        """

        return await self._repository.get_by_user_belongs(employee_id)


    async def add_review(self, data: ReviewBroker) -> Review | None:
        """The method adding new review to the data storage.

        Args:
            data (ReviewBroker): The details of the new review.

        Returns:
            Review | None: Full details of the newly added review.
        """

        return await self._repository.add_review(data)

    async def update_review(
        self,
        review_id: int,
        data: ReviewBroker,
    ) -> Review | None:
        """The method updating review data in the data storage.

        Args:
            review_id (int): The id of the review.
            data (ReviewBroker): The details of the updated review.

        Returns:
            Review | None: The updated review details.
        """

        return await self._repository.update_review(
            review_id=review_id,
            data=data,
        )

    async def update_review_status(
        self,
        review_id: int,
        data: ReviewUpdateStatus,
    ) -> Review | None:
        """The method updating review status in the data storage.

        Args:
            review_id (int): The id of the review.
            data (ReviewUpdateStatus): The details of the updated review.

        Returns:
            Review | None: The updated review details.
        """

        return await self._repository.update_review_status(
            review_id=review_id,
            data=data,
        )

    async def delete_review(self, review_id: int) -> bool:
        """The method updating removing review from the data storage.

        Args:
            review_id (int): The id of the review.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_review(review_id)