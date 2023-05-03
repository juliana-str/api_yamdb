import datetime
import re

from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели пользователей."""

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
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

    def validate_slug(self, slug):
        if not re.match(r'^[-a-zA-Z0-9_]+$', slug):
            raise serializers.ValidationError(
                'Неверный слаг!')
        return slug

    class Meta:
        fields = ('name', 'slug')
        model = Category


class CategoryGetField(serializers.SlugRelatedField):
    """Сериалайзер для поля модели категория."""
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


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


class GenreGetField(serializers.SlugRelatedField):
    """Сериалайзер для поля модели жанры."""
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели произведения."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = [
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        ]


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryGetField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = GenreGetField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    def validate_year(self, year):
        """Проверка года выпуска произведения."""
        date = datetime.date.today().strftime("%Y")
        if year > int(date):
            raise serializers.ValidationError(
                'Произведение еще не вышло!')
        return year

    class Meta:
        fields = '__all__'
        model = Title
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=('category', 'name'),
                message='У произведения может быть только одна категория!'
            ),)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        exclude = ['title']
        read_only_fields = (
            'id', 'author', 'pub_date',
        )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ['review']
        read_only_fields = (
            'id', 'author', 'pub_date',
        )
