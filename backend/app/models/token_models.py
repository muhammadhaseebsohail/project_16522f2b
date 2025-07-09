from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    exp: Optional[int] = Field(None, alias='exp')