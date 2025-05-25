from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import WatchedAnime, Userpreference
from .serializers import WatchedAnimeSerializer, UserpreferenceSerializer, RegisterSerializer
import requests
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# JWT Login View
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

# JWT Token Refresh View
class TokenRefreshViewCustom(TokenRefreshView):
    permission_classes = [AllowAny]

# Watched Anime ViewSet (Authenticated users only)
class AnimeViewSet(viewsets.ModelViewSet):
    serializer_class = WatchedAnimeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only watched anime for the logged-in user
        return WatchedAnime.objects.filter(user=self.request.user)

# User Preference ViewSet (Authenticated users only)
class UserPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = UserpreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Userpreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# AniList API Search function
ANILIST_API_URL = "https://graphql.anilist.co"

def search_anime_anilist(name=None, genre=None):
    query = '''
    query ($search: String, $genre: String) {
      Page(perPage: 10) {
        media(search: $search, genre: $genre, type: ANIME) {
          id
          title {
            romaji
            english
            native
          }
          genres
          description(asHtml: false)
          coverImage {
            large
          }
          averageScore
          episodes
          status
        }
      }
    }
    '''
    variables = {
        "search": name,
        "genre": genre,
    }
    response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables})
    response.raise_for_status()
    data = response.json()
    return data['data']['Page']['media']

# Open Search API Endpoint (No auth required)
class SearchAnimeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Disable authentication for this view

    def get(self, request):
        name = request.query_params.get('name')
        genre = request.query_params.get('genre')

        try:
            anime_list = search_anime_anilist(name=name, genre=genre)
        except requests.exceptions.RequestException:
            return Response(
                {"error": "Failed to fetch data from AniList API."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(anime_list, status=status.HTTP_200_OK)

# Protected Recommendation Endpoint (JWT required)
class RecommendAnimeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Debug print - remove in production
        print("Authenticated user:", user, "Is authenticated?", user.is_authenticated)

        if not user or not user.is_authenticated:
            return Response({"error": "User not authenticated. Please login."}, status=status.HTTP_401_UNAUTHORIZED)

        preferences = Userpreference.objects.filter(user=user)
        if not preferences.exists():
            return Response({"details": "No user preferences found."}, status=status.HTTP_404_NOT_FOUND)

        preferred_genres = []
        for pref in preferences:
            if pref.genre:
                preferred_genres.extend([g.strip() for g in pref.genre.split(',') if g.strip()])

        preferred_genres = list(set(preferred_genres))  # Remove duplicates

        if not preferred_genres:
            return Response({"details": "No preferred genres found in preferences."}, status=status.HTTP_404_NOT_FOUND)

        query = '''
        query ($genres: [String]) {
          Page(perPage: 10) {
            media(genre_in: $genres, type: ANIME, sort: POPULARITY_DESC) {
              id
              title {
                romaji
                english
                native
              }
              genres
              averageScore
              description
              coverImage {
                large
              }
            }
          }
        }
        '''

        variables = {
            "genres": preferred_genres
        }

        try:
            response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables})
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return Response(
                {"error": "Failed to fetch data from AniList."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        data = response.json()
        anime_list = data.get('data', {}).get('Page', {}).get('media', [])
        if anime_list:
            return Response(anime_list)
        else:
            return Response(
                {"details": "No recommendations found for your preferences."},
                status=status.HTTP_404_NOT_FOUND
            )
