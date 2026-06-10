"""Module containing offer service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID5

from manage_job_app.core.domain.offer import Offer, OfferBroker
from manage_job_app.infrastructure.dto.offerdto import OfferDTO


class IOfferService(ABC):
    """A class representing offer repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[OfferDTO]:
        """The method getting all offers from the repository.

        Returns:
            Iterable[OfferDTO]: All offers.
        """

    @abstractmethod
    async def get_by_id(self, offer_id: int) -> OfferDTO | None:
        """The method getting an offer by provided id.

        Args:
            offer_id (int): The ID of the offer.

        Returns:
            OfferDTO | None: The offer details.
        """

    @abstractmethod
    async def get_by_user(self, user_id: UUID5) -> Iterable[Offer]:
        """The method getting offers by user who added them.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Iterable[Offer]: The offer collection.
        """

    @abstractmethod
    async def search_by_title(self, title: str) -> Iterable[Offer]:
        """Search for offers by title.

        Args:
            title (str): The title of the offer.

        Returns:
            Iterable[Offer]: A collection of offers matching the title.
        """

    @abstractmethod
    async def add_offer(self, data: OfferBroker) -> Offer | None:
        """The method adding new offer to the data storage.

        Args:
            data (OfferBroker): The data of the new offer.

        Returns:
            Offer | None: Full details of the newly added offer.
        """

    @abstractmethod
    async def update_offer(self, offer_id: int, data: OfferBroker) -> Offer | None:
        """The method updating offer data in the data storage.

        Args:
            offer_id (int): The ID of the offer.
            data (OfferBroker): The new data for the offer.

        Returns:
            Offer | None: The updated offer details.
        """

    @abstractmethod
    async def delete_offer(self, offer_id: int) -> bool:
        """The method updating removing offer from the data storage.

        Args:
            offer_id (int): The ID of the offer.

        Returns:
            bool: Success of the operation.
        """