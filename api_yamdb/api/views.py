from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, status, permissions, serializers,
                            mixins, viewsets)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly)
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from reviews.models import Genre, Category, Title, User, Review
from .filters import TitleFilter
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModerOnly

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitleSerializer,
    UserSerializer,
    SignUpSerializer,
    TokenSerializer,
    ReviewSerializer,
    CommentSerializer,
)


class UserViewSet(ModelViewSet):
    """Вьюсет для просмотра, создания, удаления пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = ["get", "post", "patch", "delete"]

    @action(methods=('get', 'patch',), detail=False, url_path='me',
            permission_classes=(permissions.IsAuthenticated,))
    def user_own_account(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    email = serializer.validated_data["email"]

    try:
        user, created = User.objects.get_or_create(
            username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
    except IntegrityError:
        raise serializers.ValidationError(
            "Данные имя пользователя или Email уже зарегистрированы"
        )
    send_mail(
        "Код подтверждения",
        f"Ваш код подтверждения: {confirmation_code}",
        settings.EMAIL,
        [user.email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    confirmation_code = serializer.validated_data["confirmation_code"]
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = str(AccessToken.for_user(user))
        return Response({"token": token}, status=status.HTTP_200_OK)
    raise serializers.ValidationError("Введен неверный код.")


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """Вьюсет для просмотра, создания, удаления категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """Вьюсет для просмотра жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Вьюсет для просмотра, создания, удаления произведения."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-id')
    title_get_serializer_class = TitleGetSerializer
    title_serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return self.title_get_serializer_class
        return self.title_serializer_class


class ReviewViewSet(viewsets.ModelViewSet):
    """Получение/создание/обновление/удаление
    отзыва к произведению
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModerOnly,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))


class CommentViewSet(viewsets.ModelViewSet):
    """Получение/создание/обновление/удаление
    комментария к отзыву о произведении
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerOnly,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = self.get_title()
        review = get_object_or_404(Review,
                                   id=self.kwargs.get('review_id'),
                                   title=title)
        serializer.save(author=self.request.user, review=review)

    def get_title(self):
        if hasattr(self, 'title'):
            return self.title
        self.title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return self.title
