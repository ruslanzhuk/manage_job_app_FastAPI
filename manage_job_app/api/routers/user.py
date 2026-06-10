"""A module containing user endpoints."""

from typing import Iterable, Union
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from pydantic import UUID4

from manage_job_app.infrastructure.utils import consts
from manage_job_app.container import Container
from manage_job_app.core.domain.user import Employer, Employee, EmployerIn, EmployeeIn, UserIn
from manage_job_app.infrastructure.dto.userdto import EmployerDTO, EmployeeDTO
from manage_job_app.infrastructure.services.iuser import IUserService
from manage_job_app.infrastructure.dto.tokendto import TokenDTO

bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Users"])

@router.post("/employer/register", response_model=Employer, status_code=201)
@inject
async def add_employer(
    employer: EmployerIn,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """An endpoint for adding new user as employer.

    Args:
        employer (EmployerIn): The user data.
        service (IUserService, optional): The injected service dependency.

    Returns:
        dict: The new employer attributes.
    """

    if exist_user := await service.get_by_email(employer.model_dump()["email"]):
        raise HTTPException(
            status_code=400,
            detail="User with provided email already exists"
        )

    if new_employer := await service.add_user(employer):
        return new_employer.model_dump() if new_employer else {}


@router.post("/employee/register", response_model=Employee, status_code=201)
@inject
async def add_employee(
    employee: EmployeeIn,
    service: IUserService = Depends(Provide[Container.user_service]),
):
    """An endpoint for adding new user as employee.

    Args:
        employee (EmployeeIn): The user data.
        service (IUserService, optional): The injected service dependency.

    Returns:
        dict: The new employee attributes.
    """

    if exist_user := await service.get_by_email(employee.model_dump()["email"]):
        raise HTTPException(
            status_code=400,
            detail="User with provided email already exists"
        )

    if new_employee := await service.add_user(employee):
        return new_employee.model_dump() if new_employee else {}


@router.post("/token", response_model=TokenDTO, status_code=200)
@inject
async def authenticate_user(
    user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for authenticating users.

    Args:
        user (UserIn): The user input data.
.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The token DTO details.
    """

    if token_details := await service.authenticate_user(user):
        print("user confirmed")
        return token_details.model_dump()

    raise HTTPException(
        status_code=401,
        detail="Provided incorrect credentials",
    )

@router.get("/all", response_model=Iterable[Union[EmployerDTO, EmployeeDTO]], status_code=200)
@inject
async def get_all_users(
    service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable[Union[EmployerDTO, EmployeeDTO]]:
    """An endpoint for getting all users.

    Args:
        service (IUserService, optional): The injected service dependency.

    Returns:
        Iterable: The user attributes collection.
    """

    users = await service.get_all()

    return users

@router.get(
    "/employer/all",
    response_model=Iterable[EmployerDTO],
    status_code=200
)
@inject
async def get_all_employers(
    service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable[EmployerDTO]:
    """An endpoint for getting all employers.

    Args:
        service (IUserService, optional): The injected service dependency.

    Returns:
        Iterable: The employer attributes collection.
    """

    users = await service.get_all_employers()

    return users

@router.get(
    "/employee/all",
    response_model=Iterable[EmployeeDTO],
    status_code=200
)
@inject
async def get_all_employees(
    service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable[EmployeeDTO]:
    """An endpoint for getting all employees.

    Args:
        service (IUserService, optional): The injected service dependency.

    Returns:
        Iterable: The employee attributes collection.
    """

    users = await service.get_all_employees()

    return users


@router.get(
        "/{user_id}",
        response_model=Union[EmployerDTO, EmployeeDTO],
        status_code=200,
)
@inject
async def get_user_by_id(
    user_id: UUID4,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict | None:
    """An endpoint for getting user by id.

    Args:
        user_id (UUID4): The id of the user.
        service (IUserService, optional): The injected service dependency.

    Returns:
        dict | None: The user details.
    """

    if user := await service.get_by_id(user_id):
        return user.model_dump()

    raise HTTPException(status_code=404, detail="User not found")


@router.get(
        "/user/{user_name}",
        response_model=Iterable[Union[EmployerDTO, EmployeeDTO]],
        status_code=200,
)
@inject
async def find_users_by_name(
    user_name: str,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> Iterable[Union[EmployerDTO, EmployeeDTO]]:
    """An endpoint for finding users by name.

    Args:
        user_name (str): The name to search for.
        service (IUserService, optional): The injected service dependency.

    Returns:
        Iterable[User]: Users matching the name.
    """

    if users := await service.find_users_by_name(user_name):
        return users

    raise HTTPException(status_code=404, detail="Users not found")


@router.put("/employer/{user_id}", response_model=Employer, status_code=201)
@inject
async def update_employer(
    user_id: UUID4,
    updated_user: EmployerIn,
    service: IUserService = Depends(Provide[Container.user_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating user data.

    Args:
        user_id (UUID4): The id of the user.
        updated_user (UserIn): The updated user details.
        service (IUserService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if user does not exist.

    Returns:
        dict: The updated user details.
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

    if user_data := await service.get_by_id(user_id=user_id):
        if str(user_data.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        updated_data = await service.update_user(
            user_id=user_id,
            data=updated_user,
        )

        return {**updated_data.model_dump(), "id": user_id}

    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=Employee, status_code=201)
@inject
async def update_employee(
    user_id: UUID4,
    updated_user: EmployeeIn,
    service: IUserService = Depends(Provide[Container.user_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating user data.

    Args:
        user_id (UUID4): The id of the user.
        updated_user (UserIn): The updated user details.
        service (IUserService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if user does not exist.

    Returns:
        dict: The updated user details.
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

    if user_data := await service.get_by_id(user_id=user_id):
        if str(user_data.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        updated_data = await service.update_user(
            user_id=user_id,
            data=updated_user,
        )

        return {**updated_data.model_dump(), "id": user_id}

    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", status_code=204)
@inject
async def delete_user(
    user_id: UUID4,
    service: IUserService = Depends(Provide[Container.user_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting users.

    Args:
        user_id (UUID4): The id of the user.
        service (IUserService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if user does not exist.
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

    if user_data := await service.get_by_id(user_id=user_id):
        if str(user_data.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        await service.delete_user(user_id)

        return

    raise HTTPException(status_code=404, detail="User not found")