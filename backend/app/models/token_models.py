from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    full_name: str
    email: str

class UserIn(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

class UserOut(UserBase):
    disabled: bool

class Token(BaseModel):
    access_token: str = Field(..., description="The access token")
    token_type: str = Field(..., description="The type of the token")

class TokenData(BaseModel):
    username: Optional[str] = None

class OAuth2PasswordRequestForm(BaseModel):
    username: str = Field(..., description="The user's username")
    password: str = Field(..., description="The user's password")