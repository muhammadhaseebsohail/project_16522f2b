from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class DBModelMixin(BaseModel):
    id_: Optional[str] = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class TodoInDB(DBModelMixin):
    title: str
    completed: bool

class TodoIn(TodoInDB):
    pass