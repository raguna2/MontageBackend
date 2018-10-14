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

    @property
    def display_content(self):
        return f'A: {self.content}'
