from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"

class Todo(BaseModel):
    id: Optional[int] = Field(None, example=1)
    title: str = Field(..., example="Buy groceries")
    description: str = Field(..., example="Milk, Cheese, Pizza, Fruit, Tylenol")
    done: bool = Field(False, example=False)

app = FastAPI()

todos = []

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(username: str, password: str):
    if username != "admin" or password != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": username}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    to_encode = user.copy()
    to_encode.update({"exp": 60})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    return username

@app.get("/todos", response_model=List[Todo])
async def read_todos(skip: int = 0, limit: int = 100, token: str = Depends(get_current_user)):
    return todos[skip : skip + limit]

@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int, token: str = Depends(get_current_user)):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo, token: str = Depends(get_current_user)):
    todos.append(todo.dict())
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo, token: str = Depends(get_current_user)):
    for index, existing_todo in enumerate(todos):
        if existing_todo.id == todo_id:
            todos[index] = todo
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, token: str = Depends(get_current_user)):
    for index, existing_todo in enumerate(todos):
        if existing_todo.id == todo_id:
            todos.pop(index)
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Todo not found")