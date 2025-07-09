from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    name: str = Field(..., title="The name of the item", max_length=100)
    description: Optional[str] = Field(None, title="The description of the item", max_length=500)
    price: float = Field(..., title="The price of the item", ge=0)

    class Config:
        schema_extra = {
            "example": {
                "name": "Sample Item",
                "description": "This is a sample item",
                "price": 19.99
            }
        }