from pydantic import BaseModel, ConfigDict


class ReportIn(BaseModel):
    """Model representing report's DTO attributes."""
    topic: str
    content: str

class Report(ReportIn):
    """Model representing report's attributes in the database."""
    topic: str
    content: str

    model_config = ConfigDict(from_attributes=True, extra="ignore")