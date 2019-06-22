from django.db import models

from portraits.models.questions import Question
from accounts.models import MontageUser
from montage.settings.common import AUTH_USER_MODEL


class ImpressionQuerySet(models.query.QuerySet):
    def not_collaged(self):
        """collageされていないImpressionを抽出"""
        return self.filter(is_collaged=False)


class Impression(models.Model):
    objects = ImpressionQuerySet().as_manager()

    class Meta:
        verbose_name = 'Impression'
        verbose_name_plural = 'Impressions'
        ordering = ('-posted_at', )

    # 逆参照時: Question.rev_impression.all()
    # Questionがなくなったとき、画面には表示しなくなるがデータは残す
    question = models.ForeignKey(
        Question,
        related_name='rev_impression',
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    user = models.ForeignKey(
        MontageUser,
        related_name='rev_impression',
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    content = models.CharField(
        '内容',
        max_length=42,
        help_text='質問に対してその人に対して持っている印象の内容',
    )
    posted_at = models.DateTimeField(
        '投稿日', help_text='投稿された日', auto_now_add=True)
    is_collaged = models.BooleanField(
        '変更されているか',
        help_text='collageされた場合画面には表示させないためにTrueにする',
        default=False)

    def __str__(self):
        """Printしたときはcontentを返す"""
        return self.content
