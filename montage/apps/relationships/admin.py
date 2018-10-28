from django.contrib import admin

from .models import Relationship


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    fields = ['following', 'followed']
    list_display = ('id', 'following', 'followed')
