from django.contrib import admin
from .models import User, Category, Comment, Genre, Title, Review


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
    search_fields = ('username',)


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
