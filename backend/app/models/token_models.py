from typing import List, Optional
from pydantic import BaseModel, Field

class Todo(BaseModel):
    id: Optional[int] = Field(None, example=1)
    title: str = Field(..., example="Buy groceries")
    description: str = Field(..., example="Milk, Cheese, Pizza, Fruit, Tylenol")
    done: bool = Field(False, example=False)