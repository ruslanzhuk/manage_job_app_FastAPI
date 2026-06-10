"""A module containing city endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from manage_job_app.infrastructure.dto.locationdto import CityDTO
from manage_job_app.container import Container
from manage_job_app.infrastructure.services.iadmin import IAdminService
from manage_job_app.infrastructure.utils import consts
from manage_job_app.core.domain.location import City, CityIn
from manage_job_app.infrastructure.services.icity import ICityService

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Cities"])


@router.post("/create", response_model=City, status_code=201)
@inject
async def create_city(
    city: CityIn,
    service: ICityService = Depends(Provide[Container.city_service]),
    admin_service: IAdminService = Depends(Provide[Container.admin_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new countries.

    Args:
        city (cityIn): The city data.
        service (ICityService, optional): The injected service dependency.
        admin_service (IAdminService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new city attributes.
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
        raise HTTPException(status_code=403, detail="Forbidden. You haven't role creator to create city")

    new_city = await service.add_city(city)

    return new_city.model_dump() if new_city else {}


@router.get("/all", response_model=Iterable[City], status_code=200)
@inject
async def get_all_countries(
    service: ICityService = Depends(Provide[Container.city_service]),
) -> Iterable:
    """An endpoint for getting all countries.

    Args:
        service (ICityService, optional): The injected service dependency.

    Returns:
        Iterable: The city attributes collection.
    """

    countries = await service.get_all_cities()

    return countries


@router.get("/{city_id}", response_model=CityDTO, status_code=200)
@inject
async def get_city_by_id(
    city_id: int,
    service: ICityService = Depends(Provide[Container.city_service]),
) -> dict:
    """An endpoint for getting city details by id.

    Args:
        city_id (int): The id of the city.
        service (ICityService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if city does not exist.

    Returns:
        dict: The requested city attributes.
    """

    if city := await service.get_city_by_id(city_id=city_id):
        return city.model_dump()

    raise HTTPException(status_code=404, detail="City not found")


@router.get(
        "/country/{country_id}",
        response_model=list[City],
        status_code=200,
)
@inject
async def get_city_by_country(
    country_id: int,
    service: ICityService = Depends(Provide[Container.city_service]),
) -> Iterable:
    """An endpoint for getting cities by county=ry.

    Args:
        country_id (int): The id of the country.
        service (ICityService, optional): The injected service dependency.

    Returns:
        dict: The requested cities.
    """

    countries = await service.get_cities_by_country(country_id)

    return countries


@router.put("/{city_id}", response_model=City, status_code=201)
@inject
async def update_city(
    city_id: int,
    updated_city: CityIn,
    service: ICityService = Depends(Provide[Container.city_service]),
    admin_service: IAdminService = Depends(Provide[Container.admin_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating city data.

    Args:
        city_id (int): The id of the city.
        updated_city (CityIn): The updated city details.
        service (ICityService, optional): The injected service dependency.
        admin_service (IAdminService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if city does not exist.

    Returns:
        dict: The updated city data.
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
        raise HTTPException(status_code=403, detail="Forbidden. You haven't role creator to update city data")

    if await service.get_city_by_id(city_id=city_id):
        new_updated_city = await service.update_city(
            city_id=city_id,
            data=updated_city,
        )
        return new_updated_city.model_dump() if new_updated_city else {}

    raise HTTPException(status_code=404, detail="City not found")


@router.delete("/{city_id}", status_code=204)
@inject
async def delete_city(
    city_id: int,
    service: ICityService = Depends(Provide[Container.city_service]),
    admin_service: IAdminService = Depends(Provide[Container.admin_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting countries.

    Args:
        city_id (int): The id of the city.
        service (ICityService, optional): The injected service dependency.
        admin_service (IAdminService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if city does not exist.
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
        raise HTTPException(status_code=403, detail="Forbidden. You haven't role creator to delete city from db")

    if await service.get_city_by_id(city_id=city_id):
        await service.delete_city(city_id)

        return

    raise HTTPException(status_code=404, detail="City not found")