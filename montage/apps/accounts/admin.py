from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm

from accounts.models import MontageUser

from . import models


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.MontageUser


class MontageUserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    fieldsets = ((None, {
        'fields': (
            'username',
            'password',
            'display_name',
        )
    }), )
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('username', 'password1', 'password2'),
    }), )

    list_display = (
        'id',
        'username',
        'display_name',
    )
    list_filter = ('username', )
    search_fields = ['username']
    ordering = ('username', )
    filter_horizontal = ()


admin.site.register(MontageUser, MontageUserAdmin)
