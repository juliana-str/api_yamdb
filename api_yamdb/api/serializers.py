import datetime
import re

from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели пользователей."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя'
            )
        if User.objects.filter(username=value).exists():
            return serializers.ValidationError(
                'Данное имя пользователя уже существует')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            return serializers.ValidationError(
                'Данный Email уже зарегистрирован')
        return value


class SignUpSerializer(serializers.Serializer):
    """Сериализатор объектов типа User при регистрации."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True
    )
    email = serializers.EmailField(
        required=True
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор объектов типа User при получении токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели категория."""
    name = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели жанры."""
    genre = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Genre.objects.all()
    )

    def validate_slug(self):
        slug = re.match(r'^[-a-zA-Z0-9_]+$', self.genre)
        if not slug:
            raise serializers.ValidationError(
                'Неверный слаг!')
        return slug

    class Meta:
        read_only_fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели категория."""
    category = serializers.SlugRelatedField(
        slug_field='title',
        read_only=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='genre',
        read_only=True
    )

    def validate_year(self, data):
        """Проверка года выпуска произведения."""
        date = datetime.date()
        if self.context.year > date:
            raise serializers.ValidationError(
                'Произведение еще не вышло!')
        return data

    def validate_rating(self, data):
        if 0 < data > 10:
            raise serializers.ValidationError(
                'Поставьте оценку от 1 до 10!')
        return data

    class Meta:
        fields = '__all__'
        model = Category
