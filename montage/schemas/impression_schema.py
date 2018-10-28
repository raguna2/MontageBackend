from accounts.models import MontageUser
from portraits.models import Question
from portraits.models import Impression

import graphene
from graphene_django import DjangoObjectType
from .user_schema import UserType
from .question_schema import QuestionType

from rest_framework import serializers
from graphene_django.rest_framework.mutation import SerializerMutation

from django.db.transaction import atomic

import logging


class ImpressionType(DjangoObjectType):
    """ImpressionType."""
    # display_content = graphene.String(source='display_content')
    class Meta:
        """Meta."""
        model = Impression


class CreateImpressionMutation(graphene.Mutation):
    """
    Impressionの作成

    """
    id = graphene.Int()
    question = graphene.Field(QuestionType)
    user = graphene.Field(UserType)
    content = graphene.String()
    posted_at = graphene.DateTime()
    is_collaged = graphene.Boolean()

    class Arguments:
        content = graphene.String()
        user_id = graphene.Int()
        question_id = graphene.Int()

    def mutate(self, info, content, user_id, question_id):
        user = MontageUser.objects.get(id=user_id)
        question = Question.objects.get(id=question_id)
        imp = Impression.objects.create(content=content, user=user, question=question)
        imp.save()

        return CreateImpressionMutation(content=content, user_id=user_id, question_id=question_id)

class DeleteImpressionMutation(graphene.Mutation):
    """
    Impressionの削除

    IN
    ------
    mutation{
      deleteImpression(id: 4){
        id
      }
    }

    OUT
    ----
    {
      "data": {
        "deleteImpression": {
          "id": 4
        }
      }
    }

    """
    id = graphene.Int()
    question = graphene.Field(QuestionType)
    user = graphene.Field(UserType)
    content = graphene.String()
    posted_at = graphene.DateTime()
    is_collaged = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        Impression.objects.filter(id=id).delete()

        return DeleteImpressionMutation(id=id)


class Mutation(graphene.ObjectType):
    create_impression = CreateImpressionMutation.Field()
    delete_impression = DeleteImpressionMutation.Field()


class Query(graphene.ObjectType):
    impression = graphene.Field(ImpressionType, question=graphene.String())
    impressions = graphene.List(ImpressionType)

    def resolve_impression(self, question, info):
        return Impression.objects.get(question=question)

    def resolve_impressions(self, info):
        return Impression.objects.all()
