from django.contrib import admin
from .models import Impression, Hearsay


class ImpressionInline(admin.TabularInline):
    model = Impression


@admin.register(Impression)
class ImpressionAdmin(admin.ModelAdmin):
    # 入力フィールド
    fields = ['user', 'about', 'category', 'is_personal']
    # 登録したものが見れるところ
    list_display = ('about', 'category', 'appeared_at', 'updated_at', 'is_personal')
    filter_horizontal = ('user',)


class HearsayInline(admin.StackedInline):
    model = Hearsay


@admin.register(Hearsay)
class HearsayAdmin(admin.ModelAdmin):
    fields = ['impression', 'user', 'content', 'posted_at', 'is_collaged']
    list_display = ('impression', 'user', 'content', 'posted_at', 'is_collaged')
    readonly_fields = ('posted_at',)
