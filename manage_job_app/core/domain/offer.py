from datetime import datetime

from pydantic import BaseModel, ConfigDict, UUID4


class OfferIn(BaseModel):
    """Model representing offer's DTO attributes."""
    title: str
    description: str
    category: int
    job_title: str
    salary: int
    location: int

class OfferBroker(OfferIn):
    """A broker class including user in the model."""
    author_id: UUID4


class Offer(OfferBroker):
    """Model representing offer's attributes in the database."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")