"""A module containing DTO models for output offers."""

from datetime import datetime
from typing import Optional, Union, Dict, Any
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict
from manage_job_app.core.domain.report import Report


# class ReportDTO(BaseModel):
#     """A model representing DTO for report data."""
#     topic: str
#     content: str
#
#     model_config = ConfigDict(
#         from_attributes=True,
#         extra="ignore",
#         arbitrary_types_allowed=True,
#     )
#
#     # Union[Record, Dict[str, Any]]
#     @classmethod
#     def from_record(cls, record: Record) -> "ReportDTO":
#         """A method for preparing DTO instance based on DB record.
#
#         Args:
#             record (Record): The DB record.
#
#         Returns:
#             ReportDTO: The final DTO instance.
#         """
#
#         record_dict = dict(record)
#         print(record_dict)
#         topic = record_dict.get("topic")
#         content = record_dict.get("content")
#
#         return cls(
#             topic=topic,
#             content=content,
#         )

class ReportDTO:
    """A simple DTO model without Pydantic validation."""

    def __init__(self, **kwargs):
        """Constructor that accepts any key-value pairs."""
        self.__dict__.update(kwargs)

    def __repr__(self):
        """Define how the object should be represented."""
        return f"ReportDTO({self.__dict__})"

    @classmethod
    def from_record(cls, record: dict) -> "ReportDTO":
        """A method for preparing DTO instance based on DB record."""

        return cls(**record)
