from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    password: str
    disabled: bool = Field(default=False)

class Token(BaseModel):
    access_token: str
    token_type: str

class UserInDB(User):
    hashed_password: str

class Deployment(BaseModel):
    id: int
    name: str
    version: str