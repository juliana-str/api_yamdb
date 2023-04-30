import re
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from reviews.models import Category, Genre, User, Title


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели пользователей."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Данное имя пользователя уже существует')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Данный Email уже зарегистрирован')
        return value


class SignUpSerializer(serializers.Serializer):
    """Сериализатор объектов типа User при регистрации."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        required=True,
        max_length=254
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор объектов типа User при получении токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели категория."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели жанры."""

    def validate_slug(self, slug):
        if not re.match(r'^[-a-zA-Z0-9_]+$', slug):
            raise serializers.ValidationError(
                'Неверный слаг!')
        return slug

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели произведения."""
    category = CategorySerializer(required=True)
    genre = GenreSerializer(many=True, required=True)
    name = serializers.CharField(
        max_length=256
    )
    rating = 8  # calculate_rating
    year = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели произведения."""
    category = serializers.SlugRelatedField(
        slug_field='name',
        required=True,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        required=True,
        queryset=Genre.objects.all()
    )
    name = serializers.CharField(
        max_length=256
    )

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'genre', 'description')
        model = Title
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=('category', 'name'),
                message='У произведения может быть только одна категория!'
            ),)
