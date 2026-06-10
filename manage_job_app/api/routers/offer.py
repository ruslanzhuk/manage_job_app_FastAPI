"""A module containing offer endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from pydantic import UUID4

from manage_job_app.infrastructure.dto.userdto import EmployerDTO
from manage_job_app.infrastructure.utils import consts
from manage_job_app.container import Container
from manage_job_app.core.domain.offer import Offer, OfferIn, OfferBroker
from manage_job_app.infrastructure.dto.offerdto import OfferDTO
from manage_job_app.infrastructure.services.ioffer import IOfferService
from manage_job_app.infrastructure.services.iuser import IUserService


bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Offers"])



@router.post("/create", response_model=Offer, status_code=201)
@inject
async def create_offer(
    offer: OfferIn,
    service: IOfferService = Depends(Provide[Container.offer_service]),
    user_service: IUserService = Depends(Provide[Container.user_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new offer.

       Args:
           offer (OfferIn): The offer data.
           service (IOfferService, optional): The injected service dependency.
           user_service (IUserService, optional): The injected service dependency.
           credentials (HTTPAuthorizationCredentials, optional): The credentials.

       Returns:
           dict: The new offer attributes.
       """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    authorized_user = await user_service.get_by_id(user_uuid)
    if not isinstance(authorized_user, EmployerDTO):
        raise HTTPException(status_code=403, detail="Forbidden. You haven't role Employer to create offer")

    extended_offer_data = OfferBroker(
        author_id=user_uuid,
        **offer.model_dump(),
    )

    new_offer = await service.add_offer(extended_offer_data)

    return new_offer.model_dump() if new_offer else {}


@router.get("/all", response_model=Iterable[OfferDTO], status_code=200)
@inject
async def get_all_offers(
    service: IOfferService = Depends(Provide[Container.offer_service]),
) -> Iterable:
    """An endpoint for getting all offers.

    Args:
        service (IOfferService, optional): The injected service dependency.

    Returns:
        Iterable: The offer attributes collection.
    """

    offers = await service.get_all()

    return offers


@router.get(
        "/{offer_id}",
        response_model=OfferDTO,
        status_code=200,
)
@inject
async def get_offer_by_id(
    offer_id: int,
    service: IOfferService = Depends(Provide[Container.offer_service]),
) -> dict | None:
    """An endpoint for getting offer by id.

    Args:
        offer_id (int): The id of the offer.
        service (IOfferService, optional): The injected service dependency.

    Returns:
        dict | None: The offer details.
    """

    if offer := await service.get_by_id(offer_id):
        return offer.model_dump()

    raise HTTPException(status_code=404, detail="Offer not found")


@router.get(
        "/user/{user_id}",
        response_model=Iterable[Offer],
        status_code=200,
)
@inject
async def get_offer_by_user(
    user_id: UUID4,
    service: IOfferService = Depends(Provide[Container.offer_service]),
) -> Iterable:
    """An endpoint for getting offers by user who added them.

    Args:
        user_id (int): The id of the user.
        service (IOfferService, optional): The injected service dependency.

    Returns:
        Iterable: The offer details collection.
    """

    offers = await service.get_by_user(user_id)

    return offers


@router.put("/{offer_id}", response_model=Offer, status_code=201)
@inject
async def update_offer(
    offer_id: int,
    updated_offer: OfferIn,
    service: IOfferService = Depends(Provide[Container.offer_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating offer data.

    Args:
        offer_id (int): The id of the offer.
        updated_offer (OfferIn): The updated offer details.
        service (IOfferService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if offer does not exist.

    Returns:
        dict: The updated offer details.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if offer_data := await service.get_by_id(offer_id=offer_id):
        if str(offer_data.author_id.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        extended_updated_offer = OfferBroker(
            author_id=user_uuid,
            **updated_offer.model_dump(),
        )
        updated_offer_data = await service.update_offer(
            offer_id=offer_id,
            data=extended_updated_offer,
        )
        return updated_offer_data.model_dump() if updated_offer_data \
            else {}

    # if await service.get_by_id(offer_id=offer_id):
    #     await service.update_offer(
    #         offer_id=offer_id,
    #         data=updated_offer,
    #     )
    #     return {**updated_offer.model_dump(), "id": offer_id}

    raise HTTPException(status_code=404, detail="Offer not found")


@router.delete("/{offer_id}", status_code=204)
@inject
async def delete_offer(
    offer_id: int,
    service: IOfferService = Depends(Provide[Container.offer_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting offers.

    Args:
        offer_id (int): The id of the offer.
        service (IOfferService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if offer does not exist.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if offer_data := await service.get_by_id(offer_id=offer_id):
        if str(offer_data.author_id.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")
        await service.delete_offer(offer_id)

        return

    raise HTTPException(status_code=404, detail="Offer not found")