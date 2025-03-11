from sqlalchemy.orm import Session
from models import User, Anime, user_animes
from schemas import UserCreate
from auth import get_password_hash

# Create a new user
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get a user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Get a user by ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Get all animes
def get_animes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Anime).offset(skip).limit(limit).all()

# Add an anime to user's favorite list
def add_favorite_anime(db: Session, user_id: int, anime_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    anime = db.query(Anime).filter(Anime.anime_id == anime_id).first()
    
    if not user or not anime:
        return None
    
    # Check if the relationship already exists
    existing = db.query(user_animes).filter_by(
        user_id=user_id, anime_id=anime_id
    ).first()
    
    # Add only if the relationship doesn't exist
    if not existing:
        # Insert into the many-to-many relationship table
        db.execute(
            user_animes.insert().values(
                user_id=user_id,
                anime_id=anime_id
            )
        )
        db.commit()
    
    return user

# Remove an anime from user's favorite list
def remove_favorite_anime(db: Session, user_id: int, anime_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    anime = db.query(Anime).filter(Anime.anime_id == anime_id).first()
    
    if not user or not anime:
        return None
    
    # Check if the relationship exists
    existing = db.query(user_animes).filter_by(
        user_id=user_id, anime_id=anime_id
    ).first()
    
    # Remove if the relationship exists
    if existing:
        db.execute(
            user_animes.delete().where(
                user_animes.c.user_id == user_id,
                user_animes.c.anime_id == anime_id
            )
        )
        db.commit()
    
    return user

# Get favorite animes of a user
def get_favorite_animes(db: Session, user_id: int):
    # Query animes through the many-to-many relationship
    return db.query(Anime).join(
        user_animes,
        user_animes.c.anime_id == Anime.anime_id
    ).filter(
        user_animes.c.user_id == user_id
    ).all()