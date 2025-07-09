from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi_users import FastAPIUsers, models
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import JWTAuthentication
from fastapi_security import OAuth2PasswordRequestForm
from bson import ObjectId
import logging

SECRET = "SECRET"
DATABASE_URL = "mongodb://localhost:27017"

user_db = MongoDBUserDatabase(UserDB, AsyncIOMotorClient(DATABASE_URL), 'fastapi_users')

jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)

app = FastAPI()

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

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

@app.post("/todos/")
async def create_todo(todo: TodoIn, user: User = Depends(fastapi_users.current_user())):
    collection = user_db.get_collection("todos")
    todo_dict = todo.dict(by_alias=True)
    todo_dict["user_id"] = user.id
    result = await collection.insert_one(todo_dict)
    return {"id": str(result.inserted_id)}

@app.get("/todos/{todo_id}", response_model=TodoInDB)
async def read_todo(todo_id: str, user: User = Depends(fastapi_users.current_user())):
    collection = user_db.get_collection("todos")
    todo = await collection.find_one({"_id": ObjectId(todo_id), "user_id": user.id})
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, todo: TodoIn, user: User = Depends(fastapi_users.current_user())):
    collection = user_db.get_collection("todos")
    result = await collection.update_one({"_id": ObjectId(todo_id), "user_id": user.id}, {"$set": todo.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str, user: User = Depends(fastapi_users.current_user())):
    collection = user_db.get_collection("todos")
    result = await collection.delete_one({"_id": ObjectId(todo_id), "user_id": user.id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {}