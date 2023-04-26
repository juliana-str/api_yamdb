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


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели категория."""
    category = serializers.SlugRelatedField(
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

    def validate_year(self, data):
        """Проверка года выпуска произведения."""
        date = datetime.date()
        if self.context.year > date.year:
            raise serializers.ValidationError(
                'Произведение еще не вышло!')
        return data

    class Meta:
        fields = '__all__'
        model = Title
