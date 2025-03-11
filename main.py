from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, auth, anime

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
    return {"message": "Welcome to the Anime Recommendation API"}