import datetime
import re

from rest_framework import serializers

from reviews.models import Category, Genre, User, Title


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


class TokenSerializer(serializers.Serializer):
    """Сериализатор объектов типа User при получении токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели категория."""

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели жанры."""

    def validate_slug(self, slug):
        if not re.match(r'^[-a-zA-Z0-9_]+$', slug):
            raise serializers.ValidationError(
                'Неверный слаг!')
        return slug

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели произведения."""
    category = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    name = serializers.CharField()
    rating = serializers.IntegerField()
    year = serializers.IntegerField()

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
