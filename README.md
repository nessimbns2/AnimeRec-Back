# Anime Recommendation System

This project is an Anime Recommendation System built using FastAPI. It allows users to manage their favorite animes and get recommendations based on their favorite list or a specific anime name.

## Features

- User authentication and authorization
- Add and remove animes from the user's favorite list
- Get recommendations based on a specific anime name
- Get recommendations based on the user's favorite animes
- Retrieve anime information

## Project Structure

```
anime_recommendation.db
auth.py
crud.py
database.py
insert_data.py
main.py
models.py
README.md
requirements.txt
schemas.py
test.db
__pycache__/
	auth.cpython-312.pyc
	crud.cpython-312.pyc
	database.cpython-312.pyc
	main.cpython-312.pyc
	models.cpython-312.pyc
	schemas.cpython-312.pyc
routers/
	anime.py
	auth.py
	user.py
	__pycache__/
		anime.cpython-312.pyc
		auth.cpython-312.pyc
		user.cpython-312.pyc
services/
	anime_service.py
	__pycache__/
		anime_service.cpython-312.pyc
```

## Installation
## Documentation

Once the FastAPI server is running, you can access the interactive API documentation at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/anime-recommendation.git
cd anime-recommendation
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your PostgreSQL database URL:

```
DATABASE_URL=postgresql://<username>:<password>@<host>/<database>?sslmode=require
```

Replace `<username>`, `<password>`, `<host>`, and `<database>` with your PostgreSQL credentials.

5. Run the FastAPI application:

```bash
uvicorn main:app --reload
```

### User Endpoints

- **POST /users/token**: Login and get access token
- **GET /users/me**: Get current user information
- **POST /users/**: Create a new user
- **GET /users/{user_id}**: Get user by ID
- **POST /users/{user_id}/favorite/{anime_id}**: Add an anime to user's favorite list
- **GET /users/{user_id}/favorite_animes/**: Get user's favorite animes
- **DELETE /users/{user_id}/favorite/{anime_id}**: Remove an anime from user's favorite list
- **GET /users/recommend/{anime_name}**: Get anime recommendations based on a specific anime name
- **GET /users/recommend/user/{user_id}**: Get anime recommendations based on user's favorite animes

### Anime Endpoints

- **GET /anime/{anime_name}**: Get anime by name

## Services

### AnimeService

- **get_anime_info**: Mock function to get anime information
- **recommend_anime**: Recommends similar anime based on input anime names

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pandas](https://pandas.pydata.org/)

## Contact

For any inquiries, please contact [nessimbns2@gmail.com](mailto:nessimbns2@gmail.com).
