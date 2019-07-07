from django.db import models


class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=20, help_text='カテゴリを識別するための名前')
    description = models.CharField(
        '説明文', max_length=64, help_text='カテゴリの説明文', blank=True)

    def __str__(self):
        return self.name
