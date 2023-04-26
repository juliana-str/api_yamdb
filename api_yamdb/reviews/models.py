from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True)
    role = models.CharField(max_length=10)


class Category(models.Model):
    """Модель просмотра, создания и удаления категорий произведений."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель просмотра, создания и удаления жанров произведений."""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель создания, редактирования и удаления объектов."""
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='title',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    rating = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=200,
                                   null=True,
                                   blank=True)


class Genre_title(models.Model):
    genre = models.ManyToManyField(
        Genre,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True
    )


class Review(models.Model):
    """Модель создания, редактирования и удаления отзывов."""
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Comment(models.Model):
    """Модель создания, редактирования и удаления комментариев."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    review = models.ForeignKey(
        Review,
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text



