from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    IsAuthenticated)
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import filters, mixins, viewsets

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


class CommentViewSet(ModelViewSet):
    """Вьюсет для просмотра, создания, изменения, удаления комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,
                          ModeratorUser,
                          IsAdminUser,)

    def get_review(self):
        """Метод получения определенного ревью."""
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Метод получения комментариев."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Метод создания комментария."""
        serializer.save(author=self.request.user,
                        review=self.get_review())

    def destroy(self, request, *args, **kwargs):
        """Метод удаления комментария."""
        comment = get_object_or_404(
            Comment,
            pk=self.kwargs.get('comment_id')
        )
        comment.delete()


class ReviewViewSet(ModelViewSet):
    """Вьюсет для просмотра, создания ревью на произведения."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('title_id',)

    def get_queryset(self):
        """Метод получения определенного ревью."""
        return self.kwargs.get('review_id')

    def perform_create(self, serializer):
        """Метод создания ревью."""
        serializer.save(author=self.request.user,
                        pk=self.kwargs.get('review_id'))


class TitleViewSet(ModelViewSet):
    """Вьюсет для просмотра, создания, удаления категории."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (ReadOnly, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('category', 'name', 'genre', 'year',)
