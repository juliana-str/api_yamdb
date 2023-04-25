from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    IsAuthenticated)
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import filters

from .permissions import IsOwnerOrReadOnly, ReadOnly, ModeratorUser
from .serializers import (CategorySerializer, GenreSerializer,
                          CommentSerializer, TitleSerializer,
                          ReviewSerializer, UserSerializer)
from reviews.models import Genre, Review, Category, Title, User, Comment


class UserViewSet(ModelViewSet):
    """Вьюсет для просмотра, создания, удаления пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('username',)


class CategoryViewSet(ModelViewSet):
    """Вьюсет для просмотра, создания, удаления категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (ReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ModelViewSet):
    """Вьюсет для просмотра жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (ReadOnly, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    """Вьюсет для просмотра, создания, удаления категории."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (ReadOnly, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('category', 'name', 'genre', 'year',)
