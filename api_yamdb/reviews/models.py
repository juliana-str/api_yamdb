from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель просмотра, создания и удаления пользователей."""
    username = models.CharField(
        blank=False,
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        blank=False,
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=16,
        default='User',
        verbose_name='Право доступа'
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.role == 'admin'
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ('id',)


class Category(models.Model):
    """Модель просмотра, создания и удаления категорий произведений."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель просмотра, создания и удаления жанров произведений."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель создания, редактирования и удаления объектов."""
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        through='Genre_title',
        related_name='titles'
    )
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.CharField(max_length=200,
                                   null=True,
                                   blank=True)


class Genre_title(models.Model):
    """Модель связи моделей произведения и жанров."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
