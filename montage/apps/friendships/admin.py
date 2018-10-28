from django.contrib import admin

from .models import Friendship


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    fields = ['relate_from', 'relate_to']
    list_display = ('id', 'relate_from', 'relate_to')
