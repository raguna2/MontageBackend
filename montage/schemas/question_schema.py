from portraits.models import Question

import graphene
from graphene_django import DjangoObjectType


class QuestionType(DjangoObjectType):
    """QuestionType."""
    # display_about = graphene.String(source='display_about')
    class Meta:
        """Meta."""
        model = Question


class Mutation(graphene.ObjectType):
    # TODO: Mutationの追加
    pass


class Query(graphene.ObjectType):
    question = graphene.Field(QuestionType, user_id=graphene.Int())
    questions = graphene.List(QuestionType)

    def resolve_question(self, user_id, info):
        return Question.objects.get(user__pk=user_id)

    def resolve_questions(self, info):
        return Question.objects.all()
