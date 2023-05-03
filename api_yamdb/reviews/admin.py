from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


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


class TitleAdmin(admin.ModelAdmin):
    list_display = ('get_genres', )

    def get_genres(self, obj):
        return ', '.join([str(genre) for genre in obj.genres.all()])

    get_genres.short_description = 'genres'


admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
