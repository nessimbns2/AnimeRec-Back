import pandas as pd
from sqlalchemy.orm import Session
from database import engine
from models import Anime

# Read the CSV file
csv_file_path = "../Model/anime.csv"
df = pd.read_csv(csv_file_path)

# Replace NaN values with an empty string
df = df.fillna("")

# Create a new database session
session = Session(bind=engine)

# Insert data into the Anime table
for index, row in df.iterrows():
    anime = Anime(
        anime_id=row['anime_id'],
        name=row['name'],
        genre=row['genre'],
        type=row['type'],
        rating=row['rating']
    )
    session.add(anime)

# Commit the transaction
session.commit()

# Close the session
session.close()