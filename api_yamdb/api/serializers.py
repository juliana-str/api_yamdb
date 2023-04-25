import datetime
from typing import re

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


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('review', 'author')
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели жанры."""
    genre = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Genre.objects.all()
    )

    def validate_slug(self):
        slug = self.genre
        if not re.match(r'^[-a-zA-Z0-9_]+$', slug):
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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели ревью."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField()

    def validate_review(self, data):
        """Проверка повторного ревью."""
        if self.context['request'].user == data:
            raise serializers.ValidationError(
                'Вы уже оставили ревью!')
        return data

    def validate_score(self, data):
        """Проверка оценки."""
        if not 0 < data < 11:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10!')
        return data

    class Meta:
        fields = '__all__'
        model = Review
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title.name'),
                message='Вы уже оставили ревью!'
            ),)
