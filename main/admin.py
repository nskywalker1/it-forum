from django.contrib import admin
from .models import Comment, Category, Post


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)


admin.site.register(Post)

admin.site.register(Comment)
