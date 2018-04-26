from django.contrib import admin

from app.library.models import UserCategory, Category


class UserCategoryAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(UserCategory, UserCategoryAdmin)
