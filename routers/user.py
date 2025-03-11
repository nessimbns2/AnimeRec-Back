import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import verify_password
from jose import JWTError, jwt
from datetime import datetime, timedelta

from database import SessionLocal, engine
from models import Base, User as UserModel, Anime as AnimeModel, user_animes
from schemas import User, UserCreate, Anime, UserInDB
import crud
from services.anime_service import AnimeService

Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/users", tags=["users"])

anime_service = AnimeService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Secret key to encode the JWT token
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

# Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get current user
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return User.from_db_model(user)

@router.post("/token", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.create_user(db=db, user=user)
    return User.from_db_model(db_user)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User.from_db_model(db_user)

@router.post("/{user_id}/favorite/{anime_id}", response_model=User)
def add_favorite_anime(user_id: int, anime_id: int, db: Session = Depends(get_db)):
    user = crud.add_favorite_anime(db, user_id=user_id, anime_id=anime_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User or Anime not found")
    return User.from_db_model(user)

@router.get("/{user_id}/favorite_animes/", response_model=List[Anime])
def read_favorite_animes(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    favorite_animes = crud.get_favorite_animes(db, user_id=user_id)
    return favorite_animes

@router.delete("/{user_id}/favorite/{anime_id}", response_model=User)
def remove_favorite_anime(user_id: int, anime_id: int, db: Session = Depends(get_db)):
    user = crud.remove_favorite_anime(db, user_id=user_id, anime_id=anime_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User or Anime not found")
    return User.from_db_model(user)

@router.get("/recommend/{anime_name}", response_model=List[str])
def recommend_anime(anime_name: str, db: Session = Depends(get_db)):
    recommendations = anime_service.recommend_anime([anime_name], top_n=4)
    if "Error" in recommendations[0]:
        raise HTTPException(status_code=404, detail=recommendations[0])
    return recommendations

@router.get("/recommend/user/{user_id}", response_model=List[Anime])
def recommend_anime_for_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    favorite_animes = crud.get_favorite_animes(db, user_id=user_id)
    favorite_anime_names = [anime.name for anime in favorite_animes]
    recommendations = anime_service.recommend_anime(favorite_anime_names, top_n=8)
    if "Error" in recommendations[0]:
        raise HTTPException(status_code=404, detail=recommendations[0])
    recommended_animes = [db.query(AnimeModel).filter(AnimeModel.name == name).first() for name in recommendations]
    return recommended_animes


