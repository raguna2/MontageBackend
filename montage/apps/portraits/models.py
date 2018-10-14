from django.db import models

from accounts.models import MontageUser
from categories.models import Category
from montage.settings.common import AUTH_USER_MODEL


class QuestionQuerySet(models.query.QuerySet):
    def presonalized(self):
        """
        個人のページで作成された質問だけに絞る
        """
        return self.filter(is_personal=True)

    def masters(self):
        """
        運営が作成した質問だけに絞る
        """
        return self.filter(is_personal=False)


class Question(models.Model):
    objects = QuestionQuerySet().as_manager()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ('-updated_at', )

    # 逆参照時: MontageUser.rev_question.all()
    user = models.ManyToManyField(
        AUTH_USER_MODEL, related_name='rev_question')
    about = models.CharField(max_length=42, )
    # 逆参照時: Category.rev_impression.all()
    # カテゴリが削除されてもQuestionは残す
    category = models.ForeignKey(
        Category,
        related_name='rev_question',
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    appeared_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_personal = models.BooleanField(
        '個人的なものか',
        help_text="""
                  ユーザが独自に作成したものであればTrue,
                  運営が作成したものならFalse
                  """,
        default=False)

    def __str__(self):
        """printされたときはaboutを返す"""
        return self.about

    @property
    def display_about(self):
        """画面に表示するときはQ:をつける"""
        return f'Q: {self.about}'


class HearsayQuerySet(models.query.QuerySet):
    def not_collaged(self):
        """collageされていないものを抽出"""
        return self.filter(is_collaged=False)


class Hearsay(models.Model):
    objects = HearsayQuerySet().as_manager()

    class Meta:
        verbose_name = 'Hearsay'
        verbose_name_plural = 'Hearsays'
        ordering = ('-posted_at', )

    # 逆参照時: Impression.rev_hearsay.all()
    # Impressionがなくなったとき、画面には表示しなくなるがデータは残す
    impression = models.ForeignKey(
        Impression,
        related_name='rev_hearsay',
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    user = models.ForeignKey(
        MontageUser,
        related_name='rev_hearsay',
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    content = models.CharField(
        'うわさ',
        max_length=42,
        help_text='うわさの内容',
    )
    posted_at = models.DateTimeField(
        '作成日', help_text='うわさが投稿された日', auto_now_add=True)
    is_collaged = models.BooleanField(
        '変更されているか',
        help_text='collageされた場合画面には表示させないためにTrueにする',
        default=False)

    def __str__(self):
        """Printしたときはaboutを返す"""
        return self.content

    @property
    def display_content(self):
        return f'A: {self.content}'
