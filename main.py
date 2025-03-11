from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, auth, anime
from database import engine, Base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(anime.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Anime Recommendation System!"}