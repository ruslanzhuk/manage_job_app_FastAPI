from pydantic import BaseModel, ConfigDict

class CategoryIn(BaseModel):
    """Model representing category's DTO attributes."""
    name: str


class Category(CategoryIn):
    """Model representing offer's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")