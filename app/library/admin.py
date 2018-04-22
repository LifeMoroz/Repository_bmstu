from django.contrib import admin

from app.library.models import UserCategory


class UserCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserCategory, UserCategoryAdmin)
