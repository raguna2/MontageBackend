from django.db import models
from django.core import validators
from montage.settings.common import AUTH_USER_MODEL
from categories.models import Category


class ImpressionQuerySet(models.query.QuerySet):
    def presonalized(self):
        return self.filter(is_personal=True)

    def masters(self):
        return self.filter(is_personal=False)


class ImpressionManager(models.Manager):
    def get_query_set(self):
        return ImpressionQuerySet(self.model)

    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)


class Impression(models.Model):
    objects = ImpressionManager()

    class Meta:
        verbose_name = 'Impression'
        verbose_name_plural = 'Impressions'
        ordering = ('-updated_at',)

    user = models.ManyToManyField('ユーザ', AUTH_USER_MODEL, related_name='user')
    about = models.CharField(
        '質問項目',
        max_length=42,
        help_text='何のプロフィールについて?',
        validators=[validators.MinLengthValidator(5)],
        error_messages={
            'min': "質問は5文字以上で行ってください",
        },
    )
    category = models.ForeignKey('aboutのカテゴリ', Category, related_name='category')
    appeared_at = models.DateTimeField('生成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    is_personal = models.BooleanField(
        '個人的なものか',
        help_text="""
                  ユーザが独自に作成したものであればTrue,
                  運営が作成したものならFalse
                  """,
        default=False
    )

    def __str__(self):
        """printされたときはaboutを返す"""
        return self.about

    @property
    def display_about(self):
        return f'@{self.about}'


class HearsayQuerySet(models.query.QuerySet):
    def not_collaged(self):
        return self.filter(is_collaged=False)


class HearsayManager(models.Manager):
    def get_query_set(self):
        return HearsayQuerySet(self.model)

    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)


class Hearsay(models.Model):
    class Meta:
        verbose_name = 'Hearsay'
        verbose_name_plural = 'Hearsays'
        ordering = ('-posted_at',)

    impression = models.ForeignKey(
        'impressionに対するうわさ',
        Impression,
        related_name='hearsay'
    )
    content = models.CharField(
        'うわさ',
        max_length=42,
        help_text='うわさの内容',
    )
    posted_at = models.DateTimeField(
        '作成日',
        help_text='うわさが投稿された日',
        auto_now_add=True
    )
    is_collaged = models.BooleanField(
        '変更されているか',
        help_text='collageされた場合画面には表示させないためにTrueにする',
        default=False
    )

    def __str__(self):
        """Printしたときはaboutを返す"""
        return self.about

    @property
    def display_content(self):
        return f'A: {self.content}'
