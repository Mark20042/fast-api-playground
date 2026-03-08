from fastapi import FastAPI
from typing import Optional
from contextlib import asynccontextmanager
from pydantic import BaseModel
from config.database import db, ping_db

# routers
from routers.Auth import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await ping_db()
    yield

app = FastAPI(lifespan=lifespan)

# /docs to see the documentation / swagger

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_router)

# Path Parameters with Query Parameters optional
# @app.get("/greet/{name}")
# async def greet(name:str , age: Optional[int] = None):
#     return {"message": f"Hello {name} you are {age} years old"}

# Query Parameters both 
# @app.get("/greet/")
# async def greet(name: str, age: Optional[int] = None):
#     return {"message": f"Hello {name} you are {age} years old"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


# class Student(BaseModel):
#     name: str
#     age: int
#     roll: int
    
    
# @app.post("/create_student")
# async def create_student(student: Student):
#     return {
#         "name": student.name,
#         "age": student.age,
#         "roll": student.roll
#     }