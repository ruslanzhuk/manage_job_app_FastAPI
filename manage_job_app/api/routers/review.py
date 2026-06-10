"""A module containing review endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from pydantic import UUID4

from manage_job_app.infrastructure.utils import consts
from manage_job_app.container import Container
from manage_job_app.core.domain.review import Review, ReviewIn, ReviewBroker, ReviewUpdateStatus
from manage_job_app.infrastructure.dto.reviewdto import ReviewDTO
from manage_job_app.infrastructure.services.ireview import IReviewService
from manage_job_app.infrastructure.services.iuser import IUserService
from manage_job_app.infrastructure.dto.userdto import EmployerDTO


bearer_scheme = HTTPBearer()

router = APIRouter(tags=["Reviews"])



@router.post("/create", response_model=Review, status_code=201)
@inject
async def create_review(
    review: ReviewIn,
    service: IReviewService = Depends(Provide[Container.review_service]),
    user_service: IUserService = Depends(Provide[Container.user_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new review.

       Args:
           review (ReviewIn): The review data.
           service (IReviewService, optional): The injected service dependency.
           user_service (IUserService, optional): The injected service dependency.
           credentials (HTTPAuthorizationCredentials, optional): The credentials.

       Returns:
           dict: The new review attributes.
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
        raise HTTPException(status_code=403, detail="Forbidden")

    extended_review_data = ReviewBroker(
        employer_id=user_uuid,
        **review.model_dump(),
    )

    new_review = await service.add_review(extended_review_data)

    return new_review.model_dump() if new_review else {}


@router.get("/all", response_model=Iterable[ReviewDTO], status_code=200)
@inject
async def get_all_reviews(
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> Iterable:
    """An endpoint for getting all reviews.

    Args:
        service (IReviewService, optional): The injected service dependency.

    Returns:
        Iterable: The review attributes collection.
    """

    reviews = await service.get_all()

    return reviews


@router.get(
        "/{review_id}",
        response_model=ReviewDTO,
        status_code=200,
)
@inject
async def get_review_by_id(
    review_id: int,
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> dict | None:
    """An endpoint for getting review by id.

    Args:
        review_id (int): The id of the review.
        service (IReviewService, optional): The injected service dependency.

    Returns:
        dict | None: The review details.
    """

    if review := await service.get_by_id(review_id):
        return review.model_dump()

    raise HTTPException(status_code=404, detail="Review not found")


@router.get(
        "/user/{employer_id}",
        response_model=Iterable[Review],
        status_code=200,
)
@inject
async def get_review_by_user(
    user_id: UUID4,
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> Iterable:
    """An endpoint for getting reviews by user who added them.

    Args:
        user_id (UUID4): The id of the user.
        service (IReviewService, optional): The injected service dependency.

    Returns:
        Iterable: The review details collection.
    """

    reviews = await service.get_by_user(user_id)

    return reviews

@router.get(
        "/user/employee/{employee_id}",
        response_model=Iterable[Review],
        status_code=200,
)
@inject
async def get_review_by_user_as_employee(
    employee_id: UUID4,
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> Iterable:
    """An endpoint for getting reviews by user who own.

    Args:
        employee_id (UUID4): The id of the user.
        service (IReviewService, optional): The injected service dependency.

    Returns:
        Iterable: The review details collection.
    """

    reviews = await service.get_by_user_belongs(employee_id)

    return reviews


@router.put("/{review_id}", response_model=Review, status_code=201)
@inject
async def update_review(
    review_id: int,
    updated_review: ReviewIn,
    service: IReviewService = Depends(Provide[Container.review_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating review data.

    Args:
        review_id (int): The id of the review.
        updated_review (ReviewIn): The updated review details.
        service (IReviewService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if review does not exist.

    Returns:
        dict: The updated review details.
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

    if review_data := await service.get_by_id(review_id=review_id):
        if str(review_data.employer_id.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        extended_updated_review = ReviewBroker(
            employer_id=user_uuid,
            **updated_review.model_dump(),
        )
        updated_review_data = await service.update_review(
            review_id=review_id,
            data=extended_updated_review,
        )
        return updated_review_data.model_dump() if updated_review_data \
            else {}

    raise HTTPException(status_code=404, detail="Review not found")

@router.put("update_status/{review_id}", response_model=Review, status_code=201)
@inject
async def update_review_status(
    review_id: int,
    updated_review: ReviewUpdateStatus,
    service: IReviewService = Depends(Provide[Container.review_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating review status.

    Args:
        review_id (int): The id of the review.
        updated_review (ReviewUpdateStatus): The updated review details.
        service (IReviewService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if review does not exist.

    Returns:
        dict: The updated review details.
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

    if review_data := await service.get_by_id(review_id=review_id):
        if str(review_data.employee_id.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")

        extended_updated_review = ReviewUpdateStatus(
            **updated_review.model_dump(),
        )
        updated_review_data = await service.update_review_status(
            review_id=review_id,
            data=extended_updated_review,
        )
        return updated_review_data.model_dump() if updated_review_data \
            else {}

    raise HTTPException(status_code=404, detail="Review not found")



@router.delete("/{review_id}", status_code=204)
@inject
async def delete_offer(
    review_id: int,
    service: IReviewService = Depends(Provide[Container.review_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting reviews.

    Args:
        review_id (int): The id of the review.
        service (IReviewService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if review does not exist.
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

    if review_data := await service.get_by_id(review_id=review_id):
        if str(review_data.employer_id.id) != user_uuid:
            raise HTTPException(status_code=403, detail="Forbidden")
        await service.delete_review(review_id)

        return

    raise HTTPException(status_code=404, detail="Review not found")