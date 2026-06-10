"""Module containing offer repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from manage_job_app.core.domain.offer import OfferBroker

from pydantic import UUID5


class IOfferRepository(ABC):
    """An abstract class representing protocol of offer repository."""

    @abstractmethod
    async def get_all_offers(self) -> Iterable[Any]:
        """The abstract getting all offers from the data storage.

        Returns:
            Iterable[Any]: Offers in the data storage.
        """


    @abstractmethod
    async def get_by_id(self, offer_id: int) -> Any | None:
        """The abstract getting offer by provided id.

        Args:
            offer_id (int): The id of the offer.

        Returns:
            Offer | None: The offer details.
        """



    @abstractmethod
    async def get_by_user(self, user_id: UUID5) -> Iterable[Any]:
        """The abstract getting offers by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Offer]: The offer collection.
        """

    @abstractmethod
    async def search_by_title(self, title: str) -> Iterable[Any]:
        """Search for offers by title.

        Args:
            title (str): The title of the offer.

        Returns:
            Iterable[Offer]: A collection of offers matching the title.
        """

    @abstractmethod
    async def add_offer(self, data: OfferBroker) -> Any | None:
        """The abstract adding new offer to the data storage.

        Args:
            data (OfferBroker): The details of the new offer.

        Returns:
            Any | None: The newly added offer.
        """

    @abstractmethod
    async def update_offer(
        self,
        offer_id: int,
        data: OfferBroker,
    ) -> Any | None:
        """The abstract updating offer data in the data storage.

        Args:
            offer_id (int): The id of the offer.
            data (OfferBroker): The details of the updated offer.

        Returns:
            Offer | None: The updated offer details.
        """

    @abstractmethod
    async def delete_offer(self, offer_id: int) -> bool:
        """The abstract updating removing offer from the data storage.

        Args:
            offer_id (int): The id of the offer.

        Returns:
            bool: Success of the operation.
        """
