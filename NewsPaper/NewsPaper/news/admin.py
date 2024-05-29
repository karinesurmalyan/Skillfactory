from django.contrib import admin
from .models import Category, Post


class ProductAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице
    list_display = [field.name for field in Post._meta.get_fields()]  # генерируем список имён всех полей для более красивого отображения
    list_filter = ('category', 'title')
    search_fields = ('title', 'category__title')


admin.site.register(Category)
admin.site.register(Post)
