from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MangoReadPagination, CommentReadPagination
from .models import Manga, Type, Genre, Comment
from .filters import MangaFilter
from .serializers import (MangaSerializer, TypeSerializer, GenreSerializer,
                          CommentSerializer, MangoDetailSerializer,
                          )
from .permissions import IsAuthorComment


class MangaViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.action == "retrieve":
            return MangoDetailSerializer
        return MangaSerializer

    queryset = Manga.objects.all().order_by("-id")
    lookup_field = "manga_slug"
    pagination_class = MangoReadPagination
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = MangaFilter
    search_fields = ("manga_name", "mangatype__type")
    ordering_fields = ("manga_year", "release_year")



class TypeViewSet(ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().order_by("-id")
    serializer_class = CommentSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthorComment,)
    pagination_class = CommentReadPagination

