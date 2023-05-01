from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import filters, status, permissions, serializers, mixins

from api_yamdb.settings import EMAIL

from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModerOnly
from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitleSerializer,
    UserSerializer,
    SignUpSerializer,
    TokenSerializer,
)
from reviews.models import Genre, Category, Title, User


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
        send_mail(
            "Код подтверждения",
            f"Ваш код подтверждения: {confirmation_code}",
            EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    except IntegrityError:
        raise serializers.ValidationError(
            "Данные имя пользователя или Email уже зарегистрированы"
        )


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
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(ModelViewSet):
    """Вьюсет для просмотра, создания, изменения
     и удаления произведения."""
    queryset = Title.objects.all()
    Get_serializer_class = TitleGetSerializer
    Title_serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'get':
            return self.Get_serializer_class
        return self.Title_serializer_class
