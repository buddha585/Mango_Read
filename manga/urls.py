from rest_framework.routers import SimpleRouter, DefaultRouter
from django.urls import path, include
from .views import (MangaViewSet, GenreViewSet, TypeViewSet, CommentViewSet,)

ROUTER = SimpleRouter()
ROUTER.register("manga", MangaViewSet, basename="manga")
ROUTER.register("genre", GenreViewSet, basename="genre")
ROUTER.register("type", TypeViewSet, basename="type")
ROUTER.register("comment", CommentViewSet, basename="comment")
urlpatterns = [
    path("", include(ROUTER.urls)),
]