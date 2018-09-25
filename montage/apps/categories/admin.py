from django.contrib import admin
from .models import Category


class CategoryInline(admin.StackedInline):
    model = Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    list_display = ('id', 'name', 'description')
