from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_username


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


class SignUpSerializer(serializers.Serializer):
    """Сериализатор объектов типа User при регистрации."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(validate_username,)
    )
    email = serializers.EmailField(required=True, max_length=254)


class TokenSerializer(serializers.Serializer):
    """Сериализатор объектов типа User при получении токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели категория."""

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

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class GenreGetField(serializers.SlugRelatedField):
    """Сериалайзер для поля модели жанры."""

    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели произведения(только чтение)."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = [
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        ]
        read_only_fields = fields


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели произведения."""

    category = CategoryGetField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = GenreGetField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


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
