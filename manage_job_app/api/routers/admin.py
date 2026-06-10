"""A module containing admin endpoints."""

from typing import Iterable, Union
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from pydantic import UUID4

from manage_job_app.infrastructure.utils import consts
from manage_job_app.container import Container
from manage_job_app.core.domain.admin import AdminIn, Admin
from manage_job_app.infrastructure.dto.admindto import AdminDTO
from manage_job_app.infrastructure.services.iadmin import IAdminService
from manage_job_app.infrastructure.dto.tokendto import TokenDTO

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Admins"])


@router.post("admin/register", response_model=Admin, status_code=201)
@inject
async def add_admin(
    admin: AdminIn,
    service: IAdminService = Depends(Provide[Container.admin_service]),
) -> dict:
    """An endpoint for adding new admin.

    Args:
        admin (AdminIn): The admin data.
        service (IAdminService, optional): The injected service dependency.

    Returns:
        dict: The new admin attributes.
    """

    if exist_user := await service.get_admin_by_email(admin.model_dump()["email"]):
        raise HTTPException(
            status_code=400,
            detail="Admin with provided email already exists"
        )

    if new_admin := await service.add_admin(admin):
        return new_admin.model_dump() if new_admin else {}

@router.post("/token", response_model=TokenDTO, status_code=200)
@inject
async def authenticate_user(
    admin: AdminIn,
    service: IAdminService = Depends(Provide[Container.admin_service]),
) -> dict:
    """A router coroutine for authenticating admins.

    Args:
        admin (AdminIn): The admin input data.
.
        service (IAdminService, optional): The injected admin service.

    Returns:
        dict: The token DTO details.
    """

    if token_details := await service.authenticate_admin(admin):
        print("admin confirmed")
        return token_details.model_dump()

    raise HTTPException(
        status_code=401,
        detail="Provided incorrect credentials",
    )

@router.get("/all", response_model=Iterable[AdminDTO], status_code=200)
@inject
async def get_all_admins(
    service: IAdminService = Depends(Provide[Container.admin_service]),
) -> Iterable[AdminDTO]:
    """An endpoint for getting all admins.

    Args:
        service (IAdminService, optional): The injected service dependency.

    Returns:
        Iterable: The admin attributes collection.
    """

    admins = await service.get_all_admins()

    return admins


@router.get(
        "/{admin_id}",
        response_model=AdminDTO,
        status_code=200,
)
@inject
async def get_admin_by_id(
    admin_id: UUID4,
    service: IAdminService = Depends(Provide[Container.admin_service]),
) -> dict | None:
    """An endpoint for getting admin by id.

    Args:
        admin_id (UUID4): The id of the admin.
        service (IAdminService, optional): The injected service dependency.

    Returns:
        dict | None: The admin details.
    """

    if admin := await service.get_admin_by_id(admin_id):
        return admin.model_dump()

    raise HTTPException(status_code=404, detail="Admin not found")


@router.put("update/{admin_id}", response_model=Admin, status_code=201)
@inject
async def update_admin(
    admin_id: UUID4,
    updated_admin: AdminIn,
    service: IAdminService = Depends(Provide[Container.admin_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating admin data.

    Args:
        admin_id (UUID4): The id of the admin.
        updated_admin (AdminIn): The updated admin details.
        service (IAdminService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if admin does not exist.

    Returns:
        dict: The updated admin details.
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

    if admin_data := await service.get_admin_by_id(admin_id=admin_id):
        if str(admin_data.id) != admin_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        updated_data = await service.update_admin(
            admin_id=admin_id,
            data=updated_admin,
        )

        return {**updated_data.model_dump(), "id": admin_id}

    raise HTTPException(status_code=404, detail="Admin not found")


@router.delete("delete/{admin_id}", status_code=204)
@inject
async def delete_user(
    admin_id: UUID4,
    service: IAdminService = Depends(Provide[Container.admin_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting admins.

    Args:
        admin_id (UUID4): The id of the admin.
        service (IAdminService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if admin does not exist.
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

    if admin_data := await service.get_admin_by_id(admin_id=admin_id):
        if str(admin_data.id) != admin_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        await service.delete_admin(admin_id)

        return

    raise HTTPException(status_code=404, detail="Admin not found")


