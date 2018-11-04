from django.contrib import admin
from . import models

from accounts.models import MontageUser


class MontageUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'display_name',
                       'date_of_birth', 'profile_image',
                       ('email', 'mail_confirmed'),
                       ('first_name', 'last_name')
                       )
        }),
        ('Advanced options', {
            'classes': ('collapse', ),
            'fields': ('is_staff', 'is_superuser', 'is_active'),
        }),
    )
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('username', 'password1', 'password2'),
    }), )
    list_display = (
        'id',
        'username',
        'display_name',
        'is_staff',
        'is_superuser',
        'email',
        'date_of_birth',
        'mail_confirmed',
        'upper_case_name',
        'is_active',
        'created_date',
        'modified_date',
    )
    # 編集ページへのリンクをつける項目はどれか示す
    list_display_links = (('username', ))
    list_filter = ('username', )
    search_fields = ['username']
    ordering = ('username', )
    # manytomanyを一括で横に追加削除できる
    filter_horizontal = ()

    def upper_case_name(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).upper()

    upper_case_name.short_description = 'フルネーム'


admin.site.register(MontageUser, MontageUserAdmin)
