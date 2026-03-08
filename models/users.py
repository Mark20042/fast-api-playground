from pydantic import BaseModel
from typing import Optional
from beanie import Document

class User(Document):
    id: int
    name: str
    email: str
    password: str

    class Settings:
        collection_name = "users"
        
        
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    
class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    
class UserLogin(BaseModel):
    email: str
    password: str