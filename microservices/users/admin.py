from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "bio", "email", "role")
    search_fields = ("email",)
    list_filter = ("role",)
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
