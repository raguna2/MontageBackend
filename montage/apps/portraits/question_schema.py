import logging

from apps.accounts.models import MontageUser
from apps.accounts.schemas import UserType
from apps.categories.models import Category
from apps.portraits.models import Impression, Question
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
import graphene
from graphene_django import DjangoObjectType

logger = logging.getLogger(__name__)


class QuestionType(DjangoObjectType):
    """QuestionType."""

    class Meta:
        """Meta."""
        model = Question


class FilteredQuestionType(DjangoObjectType):
    """QuestionType."""
    personalized = graphene.Field(QuestionType, source='personalized')
    masters = graphene.Field(QuestionType, source='masters')

    class Meta:
        """Meta."""
        model = Question


class CreateQuestionMutation(graphene.Mutation):
    """
    Questionの作成
    """
    question = graphene.Field(FilteredQuestionType)

    class Arguments:
        about = graphene.String()

    def mutate(self, info, about):
        user_id = info.context.user.id
        try:
            user = MontageUser.objects.get(id=user_id)
        except MontageUser.DoesNotExist as e:
            logger.error(e)
            return None

        # ユーザが作成したものは自動的にmy_questionカテゴリになる
        category = Category.objects.get(name='my_question')
        # ユーザが質問を作る用のMutationなのでis_personalはデフォルト値
        question = Question.objects.create(about=about, category=category)
        # userはmanytomany
        question.user.add(user)
        question.save()
        return CreateQuestionMutation(question=question)


class DeleteQuestionMutation(graphene.Mutation):
    """
    Questionの削除
    """
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        question = Question.objects.filter(id=id)
        try:
            question.delete()
            ok = True
        except ObjectDoesNotExist as e:
            logger.error('存在しないオブジェクトは削除できません')
            logger.error(e)

        return DeleteQuestionMutation(ok=ok)


class Mutation(graphene.ObjectType):
    create_question = CreateQuestionMutation.Field()
    delete_question = DeleteQuestionMutation.Field()


class Query(graphene.ObjectType):
    category_questions = graphene.List(
        FilteredQuestionType,
        user_id=graphene.Int(),
        category_id=graphene.Int(),
        page=graphene.Int(),
        size=graphene.Int(),
    )
    questions = graphene.List(FilteredQuestionType)

    def resolve_category_questions(
            self, info, user_id, category_id, page, size):
        """ユーザのカテゴリごとの質問(未回答のみ)

        Parameters
        -----------------
        info: Any
            リクエスト

        user_id: int
            質問を取得するユーザID

        category_id: int
            取得するカテゴリのID

        page: int
            取得開始位置

        size: int
            取得件数

        Notes
        -----------------
        回答のあるImpressionのIDをrev_impressionにもたないQuestionが未回答質問

        """
        # 既に回答のあるもののIDリストを作成
        ids = Impression.objects.filter(
            user__pk=user_id
        ).values_list('id', flat=True)

        # ユーザに紐づく未回答質問のみを抽出
        category_questions = Question.objects.filter(
            category__id=category_id,
        ).exclude(
            rev_impression__id__in=ids,
        ).select_related(
            'category'
        ).prefetch_related(
            Prefetch(
                'rev_impression',
                queryset=Impression.objects.filter(user__pk=user_id)
            )
        )

        start = page * size if page > 0 else 0
        end = size + page * size if page > 0 else size
        return category_questions[start:end]

    def resolve_questions(self, info):
        return Question.objects.all()
