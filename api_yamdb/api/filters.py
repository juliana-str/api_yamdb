from django_filters import rest_framework as filters
from reviews.models import Genre, Category, Title


class CategoryFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Category
        fields = ['name', 'category']


class GenreFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug')

    class Meta:
        model = Genre
        fields = ['name', 'genre']


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ['genre', 'category']
