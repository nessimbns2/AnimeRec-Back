from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    name = Column(String(255))
    # favorite_animes field removed

class Anime(Base):
    __tablename__ = "animes"

    anime_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    genre = Column(String(255))
    type = Column(String(255))
    rating = Column(String(255))

# Keeping the many-to-many relationship table for future use if needed
user_animes = Table(
    "user_animes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("anime_id", Integer, ForeignKey("animes.anime_id"))
)