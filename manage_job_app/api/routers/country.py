"""A module containing country endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from manage_job_app.infrastructure.dto.locationdto import CountryDTO
from manage_job_app.container import Container
from manage_job_app.infrastructure.services.iadmin import IAdminService
from manage_job_app.infrastructure.utils import consts
from manage_job_app.core.domain.location import Country, CountryIn
from manage_job_app.infrastructure.services.icountry import ICountryService

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Countries"])


@router.post("/create", response_model=Country, status_code=201)
@inject
async def create_country(
    country: CountryIn,
    service: ICountryService = Depends(Provide[Container.country_service]),
    admin_service: IAdminService = Depends(Provide[Container.admin_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new countries.

    Args:
        country (CountryIn): The country data.
        service (ICountryService, optional): The injected service dependency.
        admin_service (IAdminService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new country attributes.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    admin_uuid = token_payload.get("sub")

    if not admin_uuid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    authorized_user = await admin_service.get_admin_by_id(admin_uuid)
    if not authorized_user:
        raise HTTPException(status_code=403, detail="You are not an admin to use this function!")

    if authorized_user.privileges != "creator_data":
        raise HTTPException(status_code=403, detail="Forbidden. You haven't role creator to create country")

    new_country = await service.add_country(country)

    return new_country.model_dump() if new_country else {}


@router.get("/all", response_model=Iterable[Country], status_code=200)
@inject
async def get_all_countries(
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting all countries.

    Args:
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The country attributes collection.
    """

    countries = await service.get_all_countries()

    return countries


@router.get("/{country_id}", response_model=Country, status_code=200)
@inject
async def get_country_by_id(
    country_id: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> dict:
    """An endpoint for getting country details by id.

    Args:
        country_id (int): The id of the country.
        service (ICountryService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if country does not exist.

    Returns:
        dict: The requested country attributes.
    """

    if country := await service.get_country_by_id(country_id=country_id):
        return country.model_dump()

    raise HTTPException(status_code=404, detail="Country not found")


@router.get(
        "/continent/{continent_id}",
        response_model=list[Country],
        status_code=200,
)
@inject
async def get_country_by_continent(
    continent_id: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries by continent.

    Args:
        continent_id (int): The id of the continent.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        dict: The requested countries.
    """

    countries = await service.get_countries_by_continent(continent_id)

    return countries


@router.put("/{country_id}", response_model=Country, status_code=201)
@inject
async def update_country(
    country_id: int,
    updated_country: CountryIn,
    service: ICountryService = Depends(Provide[Container.country_service]),
    admin_service: IAdminService = Depends(Provide[Container.admin_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating country data.

    Args:
        country_id (int): The id of the country.
        updated_country (CountryIn): The updated country details.
        service (ICountryService, optional): The injected service dependency.
        admin_service (IAdminService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if country does not exist.

    Returns:
        dict: The updated country data.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    admin_uuid = token_payload.get("sub")

    if not admin_uuid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    authorized_user = await admin_service.get_admin_by_id(admin_uuid)
    if not authorized_user:
        raise HTTPException(status_code=403, detail="You are not an admin to use this function!")

    if authorized_user.privileges != "creator_data":
        raise HTTPException(status_code=403, detail="Forbidden. You haven't role creator to update country data")

    if await service.get_country_by_id(country_id=country_id):
        new_updated_country = await service.update_country(
            country_id=country_id,
            data=updated_country,
        )
        return new_updated_country.model_dump() if new_updated_country else {}

    raise HTTPException(status_code=404, detail="Country not found")


@router.delete("/{country_id}", status_code=204)
@inject
async def delete_country(
    country_id: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
    admin_service: IAdminService = Depends(Provide[Container.admin_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting countries.

    Args:
        country_id (int): The id of the country.
        service (ICountryService, optional): The injected service dependency.
        admin_service (IAdminService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if country does not exist.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    admin_uuid = token_payload.get("sub")

    if not admin_uuid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    authorized_user = await admin_service.get_admin_by_id(admin_uuid)
    if not authorized_user:
        raise HTTPException(status_code=403, detail="You are not an admin to use this function!")

    if authorized_user.privileges != "creator_data":
        raise HTTPException(status_code=403, detail="Forbidden. You haven't role creator to delete country from db")

    if await service.get_country_by_id(country_id=country_id):
        await service.delete_country(country_id)

        return

    raise HTTPException(status_code=404, detail="Country not found")