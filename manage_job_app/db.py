"""A module providing database access."""

import asyncio
from datetime import timedelta

import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy import func, Enum, CheckConstraint
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

# import os

from manage_job_app.config import config

metadata = sqlalchemy.MetaData()

offer_table = sqlalchemy.Table(
    "offers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column(
        "category",
        sqlalchemy.ForeignKey("job_categories.id"),
        nullable=False,
    ),
    sqlalchemy.Column("job_title", sqlalchemy.String),
    sqlalchemy.Column("salary", sqlalchemy.Integer),
    sqlalchemy.Column(
        "location",
        sqlalchemy.ForeignKey("cities.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "author_id",
        sqlalchemy.ForeignKey("employers.id"),
        nullable=False,
    ),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=func.now(), nullable=False),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False),
)

admin_table = sqlalchemy.Table(
    "admins",
    metadata,
    sqlalchemy.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"),),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("privileges", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=func.now(), nullable=False),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now(),
                      nullable=False),
)

employer_table = sqlalchemy.Table(
    "employers",
    metadata,
    sqlalchemy.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"),),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("number", sqlalchemy.String, nullable=True),
    sqlalchemy.Column(
        "city",
        sqlalchemy.ForeignKey("cities.id"),
        nullable=True,
    ),
    sqlalchemy.Column("company_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=func.now(), nullable=False),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now(),
                      nullable=False),
)

employee_table = sqlalchemy.Table(
    "employees",
    metadata,
    sqlalchemy.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"),),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("number", sqlalchemy.String, nullable=True),
    sqlalchemy.Column(
        "city",
        sqlalchemy.ForeignKey("cities.id"),
        nullable=True,
    ),
    sqlalchemy.Column("skills", sqlalchemy.JSON, nullable=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=func.now(), nullable=False),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now(),
                      nullable=False),
)

application_table = sqlalchemy.Table(
    "applications",
    metadata,
sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "offer_id",
        sqlalchemy.ForeignKey("offers.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("employees.id"),
        nullable=False,
    ),
    sqlalchemy.Column("cover_letter", sqlalchemy.String),
    sqlalchemy.Column("status", Enum("sent", "under_review", "accepted", "rejected", name="application_status"), nullable=False, server_default="sent"),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=func.now(), nullable=False),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False),
)

review_table = sqlalchemy.Table(
    "reviews",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "employee_id",
        sqlalchemy.ForeignKey("employees.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "employer_id",
        sqlalchemy.ForeignKey("employers.id"),
        nullable=False,
    ),
    sqlalchemy.Column("rating", sqlalchemy.Integer, CheckConstraint("rating >= 1 AND rating <= 10", name="rating_check")),
    sqlalchemy.Column("review_text", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("comments", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.String, server_default="visible", nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=func.now(), nullable=False),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False),
)

continent_table = sqlalchemy.Table(
    "continents",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("alias", sqlalchemy.String),
)

country_table = sqlalchemy.Table(
    "countries",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("alias", sqlalchemy.String),
    sqlalchemy.Column(
        "continent_id",
        sqlalchemy.ForeignKey("continents.id"),
        nullable=False,
    ),
)

city_table = sqlalchemy.Table(
    "cities",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column(
        "country_id",
        sqlalchemy.ForeignKey("countries.id"),
        nullable=False,
    ),
)

category_table = sqlalchemy.Table(
    "job_categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
)


db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}:5432/{config.DB_NAME}"
)

print("db_uri", db_uri)
print("DB_HOST:", config.DB_HOST)
print("DB_NAME:", config.DB_NAME)
print("DB_USER:", config.DB_USER)
print("DB_PASSWORD:", config.DB_PASSWORD)

engine = create_async_engine(
    # DATABASE_URL,
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    # DATABASE_URL,
    db_uri,
    # force_rollback=True,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")