import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal, engine
from models import Base, Anime as AnimeModel
from schemas import Anime
import crud

Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/animes", tags=["animes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=dict)
def read_animes(
    page: int = 1,
    limit: int = 10,
    genre: Optional[str] = None,
    name: Optional[str] = None,
    order_by_rating: Optional[bool] = False,
    db: Session = Depends(get_db)
):
    logging.info(f"Fetching animes with page={page}, limit={limit}, genre={genre}, name={name}, order_by_rating={order_by_rating}")
    query = db.query(AnimeModel)
    if genre:
        query = query.filter(AnimeModel.genre.ilike(f"%{genre}%"))
    if name:
        query = query.filter(AnimeModel.name.ilike(f"%{name}%"))
    if order_by_rating:
        query = query.order_by(AnimeModel.rating.desc())
    else:
        query = query.order_by(AnimeModel.name.asc())
    total_items = query.count()
    animes = query.offset((page - 1) * limit).limit(limit).all()
    total_pages = (total_items + limit - 1) // limit
    current_page = page
    logging.info(f"Fetched {len(animes)} animes")
    return {
        "results": [Anime.from_orm(anime).dict() for anime in animes],
        "totalItems": total_items,
        "totalPages": total_pages,
        "currentPage": current_page
    }
@router.get("/anime/{anime_name}", response_model=Anime)
def get_anime_by_name(anime_name: str, db: Session = Depends(get_db)):
    anime = db.query(AnimeModel).filter(AnimeModel.name == anime_name).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    return anime
