"""Module containing review repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from manage_job_app.core.domain.review import ReviewBroker, ReviewUpdateStatus

from pydantic import UUID5


class IReviewRepository(ABC):
    """An abstract class representing protocol of review repository."""

    @abstractmethod
    async def get_all_reviews(self) -> Iterable[Any]:
        """The abstract getting all reviews from the data storage.

        Returns:
            Iterable[Review]: Reviews in the data storage.
        """


    @abstractmethod
    async def get_by_id(self, review_id: int) -> Any | None:
        """The abstract getting review by provided id.

        Args:
            review_id (int): The id of the review.

        Returns:
            Review | None: The review details.
        """


    @abstractmethod
    async def get_by_user(self, user_id: UUID5) -> Iterable[Any]:
        """The abstract getting reviews by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Review]: The review collection.
        """

    @abstractmethod
    async def get_by_user_belongs(self, employee_id: UUID5) -> Iterable[Any]:
        """The abstract getting reviews by user who own.

        Args:
            employee_id (UUID5): The id of the user who own the review.

        Returns:
            Iterable[Review]: The review collection.
        """

    @abstractmethod
    async def add_review(self, data: ReviewBroker) -> Any | None:
        """The abstract adding new review to the data storage.

        Args:
            data (ReviewBroker): The details of the new review.

        Returns:
            Any | None: The newly added review.
        """

    @abstractmethod
    async def update_review(
        self,
        review_id: int,
        data: ReviewBroker,
    ) -> Any | None:
        """The abstract updating review data in the data storage.

        Args:
            review_id (int): The id of the review.
            data (ReviewBroker): The details of the updated review.

        Returns:
            Review | None: The updated review details.
        """

    @abstractmethod
    async def update_review_status(
        self,
        review_id: int,
        data: ReviewUpdateStatus,
    ) -> Any | None:
        """The abstract updating review status in the data storage.

        Args:
            review_id (int): The id of the review.
            data (ReviewUpdateStatus): The details of the updated review.

        Returns:
            Any | None: The updated review details.
        """

    @abstractmethod
    async def delete_review(self, review_id: int) -> bool:
        """The abstract updating removing review from the data storage.

        Args:
            review_id (int): The id of the review.

        Returns:
            bool: Success of the operation.
        """
