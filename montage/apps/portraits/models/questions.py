from django.db import models

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
        default=True)

    def __str__(self):
        """printされたときはaboutを返す"""
        return self.about

    @property
    def display_about(self):
        """画面に表示するときはQ:をつける"""
        return f'Q: {self.about}'
