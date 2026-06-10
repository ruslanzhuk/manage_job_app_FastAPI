"""Module containing offer service implementation."""

from typing import Iterable

from manage_job_app.core.domain.offer import Offer, OfferBroker
from manage_job_app.core.repositories.ioffer import IOfferRepository
from manage_job_app.infrastructure.dto.offerdto import OfferDTO
from manage_job_app.infrastructure.services.ioffer import IOfferService

from pydantic import UUID5


class OfferService(IOfferService):
    """A class implementing the offer service."""

    _repository: IOfferRepository

    def __init__(self, repository: IOfferRepository) -> None:
        """The initializer of the `offer service`.

        Args:
            repository (IOfferRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[OfferDTO]:
        """The method getting all offers from the repository.

        Returns:
            Iterable[OfferDTO]: All offers.
        """

        return await self._repository.get_all_offers()


    async def get_by_id(self, offer_id: int) -> OfferDTO | None:
        """The method getting offer by provided id.

        Args:
            offer_id (int): The id of the offer.

        Returns:
            OfferDTO | None: The offer details.
        """

        return await self._repository.get_by_id(offer_id)


    async def get_by_user(self, user_id: UUID5) -> Iterable[Offer]:
        """The method getting offers by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Airport]: The offer collection.
        """

        return await self._repository.get_by_user(user_id)

    async def search_by_title(self, title: str) -> Iterable[Offer]:
        """Search for offers by title.

        Args:
            title (str): The title of the offer.

        Returns:
            Iterable[Offer]: A collection of offers matching the title.
        """
        return await self._repository.search_by_title(title)


    async def add_offer(self, data: OfferBroker) -> Offer | None:
        """The method adding new offer to the data storage.

        Args:
            data (OfferBroker): The details of the new offer.

        Returns:
            Offer | None: Full details of the newly added offer.
        """

        return await self._repository.add_offer(data)

    async def update_offer(
        self,
        offer_id: int,
        data: OfferBroker,
    ) -> Offer | None:
        """The method updating offer data in the data storage.

        Args:
            offer_id (int): The id of the offer.
            data (OfferBroker): The details of the updated offer.

        Returns:
            Offer | None: The updated offer details.
        """

        return await self._repository.update_offer(
            offer_id=offer_id,
            data=data,
        )

    async def delete_offer(self, offer_id: int) -> bool:
        """The method updating removing offer from the data storage.

        Args:
            offer_id (int): The id of the offer.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_offer(offer_id)