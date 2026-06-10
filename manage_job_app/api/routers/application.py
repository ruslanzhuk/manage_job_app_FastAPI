"""A module containing application endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from pydantic import UUID4

from manage_job_app.infrastructure.dto.userdto import EmployeeDTO
from manage_job_app.infrastructure.utils import consts
from manage_job_app.container import Container
from manage_job_app.core.domain.application import Application, ApplicationIn, ApplicationBroker, \
    ApplicationUpdateStatus
from manage_job_app.infrastructure.dto.applicationdto import ApplicationDTO
from manage_job_app.infrastructure.services.iapplication import IApplicationService
from manage_job_app.infrastructure.services.iuser import IUserService


bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Applications"])



@router.post("/create", response_model=Application, status_code=201)
@inject
async def create_application(
    application: ApplicationIn,
    service: IApplicationService = Depends(Provide[Container.application_service]),
    user_service: IUserService = Depends(Provide[Container.user_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new application.

       Args:
           application (ApplicationIn): The application data.
           service (IApplicationService, optional): The injected service dependency.
           credentials (HTTPAuthorizationCredentials, optional): The credentials.

       Returns:
           dict: The new application attributes.
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
    if not isinstance(authorized_user, EmployeeDTO):
        raise HTTPException(status_code=403, detail="Forbidden. You haven't role  Employee role to submit an application")

    extended_application_data = ApplicationBroker(
        user_id=user_uuid,
        **application.model_dump(),
    )

    new_application = await service.add_application(extended_application_data)

    return new_application.model_dump() if new_application else {}


@router.get("/all", response_model=Iterable[ApplicationDTO], status_code=200)
@inject
async def get_all_applications(
    service: IApplicationService = Depends(Provide[Container.application_service]),
) -> Iterable:
    """An endpoint for getting all applications.

    Args:
        service (IApplicationService, optional): The injected service dependency.

    Returns:
        Iterable: The application attributes collection.
    """

    applications = await service.get_all()

    return applications


@router.get(
        "/{application_id}",
        response_model=ApplicationDTO,
        status_code=200,
)
@inject
async def get_application_by_id(
    application_id: int,
    service: IApplicationService = Depends(Provide[Container.application_service]),
) -> dict | None:
    """An endpoint for getting application by id.

    Args:
        application_id (int): The id of the application.
        service (IApplicationService, optional): The injected service dependency.

    Returns:
        dict | None: The application details.
    """

    if application := await service.get_by_id(application_id):
        return application.model_dump()

    raise HTTPException(status_code=404, detail="Application not found")


@router.get(
        "/user/{user_id}",
        response_model=Iterable[Application],
        status_code=200,
)
@inject
async def get_application_by_user(
    user_id: UUID4,
    service: IApplicationService = Depends(Provide[Container.application_service]),
) -> Iterable:
    """An endpoint for getting applications by user who added them.

    Args:
        user_id (int): The id of the user.
        service (IApplicationService, optional): The injected service dependency.

    Returns:
        Iterable: The application details collection.
    """

    applications = await service.get_by_user(user_id)

    return applications


@router.put("/{application_id}", response_model=Application, status_code=201)
@inject
async def update_application(
    application_id: int,
    updated_application: ApplicationIn,
    service: IApplicationService = Depends(Provide[Container.application_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating application data.

    Args:
        application_id (int): The id of the application.
        updated_application (ApplicationIn): The updated application details.
        service (IApplicationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if application does not exist.

    Returns:
        dict: The updated application details.
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

    if application_data := await service.get_by_id(application_id=application_id):
        if str(application_data.user_id.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        extended_updated_application = ApplicationBroker(
            user_id=user_uuid,
            **updated_application.model_dump(),
        )

        updated_application_data = await service.update_application(
            application_id=application_id,
            data=extended_updated_application,
        )
        return updated_application_data.model_dump() if updated_application_data \
            else {}

    raise HTTPException(status_code=404, detail="Application not found")

@router.put("/update_status/{application_id}", response_model=Application, status_code=201)
@inject
async def update_application_status(
    application_id: int,
    updated_application: ApplicationUpdateStatus,
    service: IApplicationService = Depends(Provide[Container.application_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating application status.

    Args:
        application_id (int): The id of the application.
        updated_application (ApplicationUpdateStatus): The updated application details.
        service (IApplicationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if application does not exist.

    Returns:
        dict: The updated application details.
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

    if application_data := await service.get_by_id(application_id=application_id):
        if str(application_data.offer_id.author_id.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        extended_updated_application = ApplicationUpdateStatus(
            **updated_application.model_dump(),
        )

        updated_application_data = await service.update_application_status(
            application_id=application_id,
            data=extended_updated_application,
        )
        return updated_application_data.model_dump() if updated_application_data \
            else {}

    raise HTTPException(status_code=404, detail="Application not found")

@router.delete("/{application_id}", status_code=204)
@inject
async def delete_application(
    application_id: int,
    service: IApplicationService = Depends(Provide[Container.application_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting applications.

    Args:
        application_id (int): The id of the application.
        service (IApplicationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if application does not exist.
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

    if application_data := await service.get_by_id(application_id=application_id):
        if str(application_data.user_id.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        await service.delete_application(application_id)

        return

    raise HTTPException(status_code=404, detail="Application not found")