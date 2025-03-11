from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserInDB(BaseModel):
    id: int
    email: EmailStr
    name: str
    
    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    email: EmailStr
    name: str
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_db_model(cls, db_user: UserInDB):
        return cls(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name
        )

class Anime(BaseModel):
    anime_id: int
    name: str
    genre: str
    type: str
    rating: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            anime_id=obj.anime_id,
            name=obj.name,
            genre=obj.genre,
            type=obj.type,
            rating=obj.rating
        )