from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    LoginView,
    TokenRefreshViewCustom,
    AnimeViewSet,
    UserPreferenceViewSet,
    SearchAnimeView,
    RecommendAnimeView,
)

router = DefaultRouter()
router.register(r'anime', AnimeViewSet, basename='anime')
router.register(r'userpreferences', UserPreferenceViewSet, basename='userpreferences')

urlpatterns = [
    # Auth routes
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshViewCustom.as_view(), name='token_refresh'),

    # API routes for anime and user preferences (viewsets via router)
    path('', include(router.urls)),

    # Search anime (open to all)
    path('anime/search/', SearchAnimeView.as_view(), name='search_anime'),

    # Recommend anime (authenticated users only)
    path('anime/recommendations/', RecommendAnimeView.as_view(), name='recommend_anime'),
]
