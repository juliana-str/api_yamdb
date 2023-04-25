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
