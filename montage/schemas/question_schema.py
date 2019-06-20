from django.core.exceptions import ObjectDoesNotExist

from accounts.models import MontageUser
from portraits.models.questions import Question
from categories.models import Category
from .user_schema import UserType

import graphene
from graphene_django import DjangoObjectType

from montage.apps.logging import logger_e


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
        user = MontageUser.objects.get(id=user_id)
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
        except ObjectDoesNotExist:
            logger_e.error('存在しないオブジェクトは削除できません')

        return DeleteQuestionMutation(ok=ok)


class Mutation(graphene.ObjectType):
    create_question = CreateQuestionMutation.Field()
    delete_question = DeleteQuestionMutation.Field()


class Query(graphene.ObjectType):
    question = graphene.Field(FilteredQuestionType, user_id=graphene.Int())
    questions = graphene.List(FilteredQuestionType)

    def resolve_question(self, user_id, info):
        return Question.objects.get(user__pk=user_id)

    def resolve_questions(self, info):
        return Question.objects.all()
