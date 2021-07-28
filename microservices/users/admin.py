from django.contrib import admin
from .models import User
from ..titles.models import Title, Genre, Category
from ..reviews.models import Review, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "bio", "email", "role")
    search_fields = ("email",)
    list_filter = ("role",)
    empty_value_display = "-пусто-"


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk", "name", "slug"
    )
    search_fields = ("name",)
    list_filter = ("name",)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "pk", "name", "slug"
    )
    search_fields = ("name",)
    list_filter = ("name",)


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "pk", "name", "category", "year", "description", "get_genre"
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"

    def get_genre(self, obj):
        return "\n".join([item.slug for item in obj.genre.all()])
    get_genre.short_description = 'Жанры'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "pk", "text", "author", "score", "pub_date", "title"
    )
    search_fields = ("author",)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author", "review", "text", "pub_date"
    )


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
