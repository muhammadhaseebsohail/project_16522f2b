from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging
import secrets

app = FastAPI()
security = HTTPBasic()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401, detail="Incorrect email or password", headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

@app.post("/item/", response_model=Item)
def create_item(item: Item, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    logger = logging.getLogger("uvicorn.error")
    try:
        return item
    except Exception as e:
        logger.error(f"Failed to create item: {e}")
        raise HTTPException(status_code=500, detail="Failed to create item")

@app.get("/item/{item_id}", response_model=Item)
def read_item(item_id: int, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    logger = logging.getLogger("uvicorn.error")
    try:
        item = {"name": "item"+str(item_id), "price": 100.0}
        return item
    except Exception as e:
        logger.error(f"Failed to read item: {e}")
        raise HTTPException(status_code=500, detail="Failed to read item")

@app.put("/item/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    logger = logging.getLogger("uvicorn.error")
    try:
        item.name = "item"+str(item_id)
        return item
    except Exception as e:
        logger.error(f"Failed to update item: {e}")
        raise HTTPException(status_code=500, detail="Failed to update item")

@app.delete("/item/{item_id}", response_class=JSONResponse)
def delete_item(item_id: int, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    logger = logging.getLogger("uvicorn.error")
    try:
        return {"message": "Item successfully deleted"}
    except Exception as e:
        logger.error(f"Failed to delete item: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete item")