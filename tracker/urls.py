from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    MiniProjectListCreateView,
    MiniProjectUpdateView,
    UserViewSet,
    MiniProjectViewSet,
)

# DRF Router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'all-projects', MiniProjectViewSet, basename='all-projects')

urlpatterns = [
    # Auth & Registration
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Role-based Project APIs
    path("projects/", MiniProjectListCreateView.as_view(), name="projects_list_create"),
    path("projects/<int:pk>/", MiniProjectUpdateView.as_view(), name="projects_update"),

    # Read-only browsing (Users + Projects)
    path("", include(router.urls)),
]
