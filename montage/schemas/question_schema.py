import logging

import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphene_django import DjangoObjectType

from accounts.models import MontageUser
from categories.models import Category
from portraits.models.impressions import Impression
from portraits.models.questions import Question

from .user_schema import UserType

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
        category_name=graphene.String(),
        page=graphene.Int(),
        size=graphene.Int(),
    )
    questions = graphene.List(FilteredQuestionType)

    def resolve_category_questions(self, info, user_id, category_name, page, size):
        """ユーザのカテゴリごとの質問(未回答のみ)

        Notes
        -----------------
        入出力値についてはsnapshotを参照

        """
        category_questions = Question.objects.filter(
            user__pk=user_id,
            category__name=category_name,
            rev_impression__isnull=True,
        )

        start = page * size if page > 0 else 0
        end = size + page * size if page > 0 else size
        return category_questions[start:end]

    def resolve_questions(self, info):
        return Question.objects.all()
