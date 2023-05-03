from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    search_fields = ('username',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('get_genres', 'get_categories', )

    def get_genres(self, obj):
        return ', '.join([str(genre) for genre in obj.genre.all()])

    def get_categories(self, obj):
        return ', '.join([str(category) for category in obj.category.all()])

    get_genres.short_description = 'genres'
    get_categories.short_description = 'categories'


admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
