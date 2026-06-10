"""Module containing review service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID5

from manage_job_app.core.domain.review import Review, ReviewBroker, ReviewUpdateStatus
from manage_job_app.infrastructure.dto.reviewdto import ReviewDTO


class IReviewService(ABC):
    """A class representing review repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[ReviewDTO]:
        """The method getting all reviews from the repository.

        Returns:
            Iterable[ReviewDTO]: All reviews.
        """

    @abstractmethod
    async def get_by_id(self, review_id: int) -> ReviewDTO | None:
        """The method getting an review by provided id.

        Args:
            review_id (int): The ID of the review.

        Returns:
            ReviewDTO | None: The review details.
        """

    @abstractmethod
    async def get_by_user(self, user_id: UUID5) -> Iterable[Review]:
        """The method getting reviews by user who added them.

        Args:
            user_id (UUID5): The ID of the user.

        Returns:
            Iterable[Review]: The review collection.
        """

    @abstractmethod
    async def get_by_user_belongs(self, employee_id: UUID5) -> Iterable[Review]:
        """The method getting reviews by user who own.

        Args:
            employee_id (UUID5): The ID of the user who own the review.

        Returns:
            Iterable[Review]: The review collection.
        """

    @abstractmethod
    async def add_review(self, data: ReviewBroker) -> Review | None:
        """The method adding new review to the data storage.

        Args:
            data (ReviewBroker): The data of the new review.

        Returns:
            Review | None: Full details of the newly added review.
        """

    @abstractmethod
    async def update_review(self, review_id: int, data: ReviewBroker) -> Review | None:
        """The method updating review data in the data storage.

        Args:
            review_id (int): The ID of the review.
            data (ReviewBroker): The new data for the review.

        Returns:
            Review | None: The updated review details.
        """

    @abstractmethod
    async def update_review_status(self, review_id: int, data: ReviewUpdateStatus) -> Review | None:
        """The method updating review status in the data storage.

        Args:
            review_id (int): The ID of the review.
            data (ReviewUpdateStatus): The new data for the review.

        Returns:
            Review | None: The updated review details.
        """

    @abstractmethod
    async def delete_review(self, review_id: int) -> bool:
        """The method updating removing review from the data storage.

        Args:
            review_id (int): The ID of the review.

        Returns:
            bool: Success of the operation.
        """