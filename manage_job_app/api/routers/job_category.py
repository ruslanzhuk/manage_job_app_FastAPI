"""A module containing category endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from manage_job_app.infrastructure.dto.job_categorydto import CategoryDTO
from manage_job_app.container import Container
from manage_job_app.infrastructure.services.iadmin import IAdminService
from manage_job_app.infrastructure.utils import consts
from manage_job_app.core.domain.job_category import Category, CategoryIn
from manage_job_app.infrastructure.services.ijob_category import ICategoryService

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Categories"])


@router.post("/create", response_model=Category, status_code=201)
@inject
async def create_category(
    category: CategoryIn,
    service: ICategoryService = Depends(Provide[Container.category_service]),
    admin_service: IAdminService = Depends(Provide[Container.admin_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new job categories.

    Args:
        category (CategoryIn): The job category data.
        service (ICategoryService, optional): The injected service dependency.
        admin_service (IAdminService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new job category attributes.
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
        raise HTTPException(status_code=403, detail="Forbidden. You haven't role creator to create category")

    new_category = await service.add_category(category)

    return new_category.model_dump() if new_category else {}


@router.get("/all", response_model=Iterable[CategoryDTO], status_code=200)
@inject
async def get_all_countries(
    service: ICategoryService = Depends(Provide[Container.category_service]),
) -> Iterable:
    """An endpoint for getting all job categories.

    Args:
        service (ICategoryService, optional): The injected service dependency.

    Returns:
        Iterable: The job category attributes collection.
    """

    categories = await service.get_all_categories()

    return categories


@router.get("/{category_id}", response_model=CategoryDTO, status_code=200)
@inject
async def get_category_by_id(
    category_id: int,
    service: ICategoryService = Depends(Provide[Container.category_service]),
) -> dict:
    """An endpoint for getting job category details by id.

    Args:
        category_id (int): The id of the job category.
        service (ICategoryService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if job
         does not exist.

    Returns:
        dict: The requested job category attributes.
    """

    if category := await service.get_category_by_id(category_id=category_id):
        return category.model_dump()

    raise HTTPException(status_code=404, detail="category not found")


@router.get(
        "/continent/{continent_id}",
        response_model=CategoryDTO,
        status_code=200,
)
@inject
async def get_category_by_offer(
    offer_id: int,
    service: ICategoryService = Depends(Provide[Container.category_service]),
) -> Iterable:
    """An endpoint for getting job category by offer.

    Args:
        offer_id (int): The id of the offer.
        service (ICategoryService, optional): The injected service dependency.

    Returns:
        dict: The requested job category.
    """

    category = await service.get_category_by_offer(offer_id)

    return category


@router.put("/{category_id}", response_model=Category, status_code=201)
@inject
async def update_category(
    category_id: int,
    updated_category: CategoryIn,
    service: ICategoryService = Depends(Provide[Container.category_service]),
    admin_service: IAdminService = Depends(Provide[Container.admin_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating job category data.

    Args:
        category_id (int): The id of the job category.
        updated_category (CategoryIn): The updated job category details.
        service (ICategoryService, optional): The injected service dependency.
        admin_service (IAdminService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if job category does not exist.

    Returns:
        dict: The updated job category data.
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
        raise HTTPException(status_code=403, detail="Forbidden. You haven't role creator to update category data")

    if await service.get_category_by_id(category_id=category_id):
        new_updated_category = await service.update_category(
            category_id=category_id,
            data=updated_category,
        )
        return new_updated_category.model_dump() if new_updated_category else {}

    raise HTTPException(status_code=404, detail="category not found")


@router.delete("/{category_id}", status_code=204)
@inject
async def delete_category(
    category_id: int,
    service: ICategoryService = Depends(Provide[Container.category_service]),
    admin_service: IAdminService = Depends(Provide[Container.admin_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting job categories.

    Args:
        category_id (int): The id of the job category.
        service (ICategoryService, optional): The injected service dependency.
        admin_service (IAdminService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if job category does not exist.
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
        raise HTTPException(status_code=403, detail="Forbidden. You haven't role creator to delete category from db")

    if await service.get_category_by_id(category_id=category_id):
        await service.delete_category(category_id)

        return

    raise HTTPException(status_code=404, detail="category not found")