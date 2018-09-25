from django.contrib import admin
from .models import Impression, Hearsay


class ImpressionInline(admin.TabularInline):
    model = Impression


@admin.register(Impression)
class ImpressionAdmin(admin.ModelAdmin):
    # fields = ['about', 'category', 'appeared_at', 'updated_at']
    # 入力フィールド
    fields = ['about', 'category', 'is_personal']
    # 登録したものが見れるところ
    list_display = ('about', 'category', 'appeared_at', 'updated_at', 'is_personal')


class HearsayInline(admin.StackedInline):
    model = Hearsay


@admin.register(Hearsay)
class HearsayAdmin(admin.ModelAdmin):
    fields = ['content', 'is_collaged']
    list_display = ('content', 'posted_at', 'is_collaged')
    list_filter = ['is_collaged']
