Anime Recommendation System
A Django REST API project for anime recommendations. Users can register, login, search anime from AniList API, save preferences, and get personalized recommendations based on preferred genres. Authentication uses JWT tokens.

Features
User registration and login with JWT authentication

Search anime by name or genre (public endpoint)

Save and manage user preferences (authenticated)

Get anime recommendations based on saved preferences (authenticated)

Integration with AniList GraphQL API

Setup and Run Locally
Prerequisites
Python 3.9+

pip

Git

Clone the repository
bash
Copy
Edit
git clone https://github.com/your-github-username/your-repo-name.git
cd your-repo-name
Create virtual environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
Apply migrations
bash
Copy
Edit
python manage.py migrate
Create a superuser (optional)
bash
Copy
Edit
python manage.py createsuperuser
Run the server
bash
Copy
Edit
python manage.py runserver
API will be at http://127.0.0.1:8000/

API Endpoints and Sample Requests/Responses
Authentication
Endpoint	Method	Description	Auth Required
/auth/register/	POST	Register a new user	No
/auth/login/	POST	Obtain JWT access and refresh tokens	No
/auth/token/refresh/	POST	Refresh access token	No

Register
Request:

http
Copy
Edit
POST /auth/register/
Content-Type: application/json

{
  "username": "user1",
  "email": "user1@example.com",
  "password": "StrongPass123"
}
Response (201 Created):

json
Copy
Edit
{
  "id": 1,
  "username": "user1",
  "email": "user1@example.com"
}
Login
Request:

http
Copy
Edit
POST /auth/login/
Content-Type: application/json

{
  "username": "user1",
  "password": "StrongPass123"
}
Response (200 OK):

json
Copy
Edit
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh...refresh_token_here...",
  "access": "eyJ0eXAiOiJKV1QiLCJh...access_token_here..."
}
Refresh Token
Request:

http
Copy
Edit
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh...refresh_token_here..."
}
Response (200 OK):

json
Copy
Edit
{
  "access": "eyJ0eXAiOiJKV1QiLCJh...new_access_token_here..."
}
Anime Search (Public)
Endpoint	Method	Description	Auth Required
/anime/search/	GET	Search anime by name or genre query params	No

Example Request:

pgsql
Copy
Edit
GET /anime/search/?name=Naruto
Response (200 OK):

json
Copy
Edit
[
  {
    "id": 20,
    "title": {
      "romaji": "Naruto",
      "english": "Naruto",
      "native": "ナルト"
    },
    "genres": ["Action", "Adventure", "Shounen"],
    "description": "Naruto Uzumaki is a young ninja...",
    "coverImage": {
      "large": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx20.jpg"
    },
    "averageScore": 79,
    "episodes": 220,
    "status": "FINISHED"
  }
]
User Preferences (Authenticated)
Endpoint	Method	Description	Auth Required
/userpreferences/	GET	List preferences of logged-in user	Yes
/userpreferences/	POST	Create a new preference	Yes

Example Create Request:

http
Copy
Edit
POST /userpreferences/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "genre": "Action, Adventure"
}
Response (201 Created):

json
Copy
Edit
{
  "id": 1,
  "user": 1,
  "genre": "Action, Adventure"
}
Watched Anime (Authenticated)
Endpoint	Method	Description	Auth Required
/watchedanime/	GET	List watched anime for logged-in user	Yes
/watchedanime/	POST	Add a watched anime entry	Yes

Example Create Request:

http
Copy
Edit
POST /watchedanime/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "anime_id": 20,
  "status": "Completed",
  "rating": 8
}
Response (201 Created):

json
Copy
Edit
{
  "id": 1,
  "user": 1,
  "anime_id": 20,
  "status": "Completed",
  "rating": 8
}
Recommendations (Authenticated)
Endpoint	Method	Description	Auth Required
/recommendations/	GET	Get anime recommendations based on user preferences	Yes

Example Request:

http
Copy
Edit
GET /recommendations/
Authorization: Bearer <access_token>
Response (200 OK):

json
Copy
Edit
[
  {
    "id": 30,
    "title": {
      "romaji": "One Piece",
      "english": "One Piece",
      "native": "ワンピース"
    },
    "genres": ["Action", "Adventure", "Fantasy"],
    "averageScore": 88,
    "description": "Follows the adventures of Monkey D. Luffy...",
    "coverImage": {
      "large": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx30.jpg"
    }
  }
]
