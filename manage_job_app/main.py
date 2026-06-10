"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.exception_handlers import http_exception_handler

from manage_job_app.api.routers.offer import router as offer_router
from manage_job_app.api.routers.user import router as user_router
from manage_job_app.api.routers.application import router as application_router
from manage_job_app.api.routers.review import router as review_router
from manage_job_app.api.routers.report import router as report_router
from manage_job_app.api.routers.continent import router as continent_router
from manage_job_app.api.routers.country import router as country_router
from manage_job_app.api.routers.city import router as city_router
from manage_job_app.api.routers.job_category import router as category_router
from manage_job_app.api.routers.admin import router as admin_router
from manage_job_app.container import Container
from manage_job_app.db import database
from manage_job_app.db import init_db



container = Container()
container.wire(modules=[
    "manage_job_app.api.routers.offer",
    "manage_job_app.api.routers.user",
    "manage_job_app.api.routers.application",
    "manage_job_app.api.routers.review",
    "manage_job_app.api.routers.report",
    "manage_job_app.api.routers.continent",
    "manage_job_app.api.routers.country",
    "manage_job_app.api.routers.city",
    "manage_job_app.api.routers.job_category",
    "manage_job_app.api.routers.admin",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(
    swagger_ui_parameters={"docExpansion": "none", "filter": True, "tryItOutEnabled": False},
    title="Job search API",
    lifespan=lifespan,
    description="API for easy job search. Employers can post their job offers "
                "to hire workers, while job seekers can apply for jobs that meet the requirements.",
    version="1.1.9"
)
app.include_router(offer_router, prefix="/offer")
app.include_router(user_router, prefix="/user")
app.include_router(application_router, prefix="/application")
app.include_router(review_router, prefix="/review")
app.include_router(report_router, prefix="/report")
app.include_router(continent_router, prefix="/continent")
app.include_router(country_router, prefix="/country")
app.include_router(city_router, prefix="/city")
app.include_router(category_router, prefix="/category")
app.include_router(admin_router, prefix="/admin")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)
