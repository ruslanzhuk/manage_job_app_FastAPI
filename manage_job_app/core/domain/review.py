from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, UUID4, conint


class ReviewIn(BaseModel):
    """Model representing review's DTO attributes."""
    employee_id: UUID4
    rating: conint(ge=1, le=10)
    review_text: str
    comments: Optional[str] = None

class ReviewBroker(ReviewIn):
    """A broker class including user in the model."""
    employer_id: UUID4

class ReviewUpdateStatus(BaseModel):
    """Model representing the field for updating review status."""
    status: Literal["visible", "hidden"]

class Review(ReviewBroker):
    """Model representing review's attributes in the database."""
    id: int
    status: Literal["visible", "hidden"] = "visible"
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")