from django.core.exceptions import ObjectDoesNotExist

from accounts.models import MontageUser
from portraits.models import Question
from portraits.models import Impression

import graphene
from graphene_django import DjangoObjectType


class ImpressionType(DjangoObjectType):
    """ImpressionType."""

    class Meta:
        """Meta."""
        model = Impression


class CreateImpressionMutation(graphene.Mutation):
    """
    Impressionの作成

    IN
    ------
    mutation{
      createImpression(userId: 1, questionId: 22, content: "質問への回答"){
        impression{
          id
          question{
            about
          }
          content
        }
      }
    }
    """
    impression = graphene.Field(ImpressionType)
    ok = graphene.Boolean()

    class Input:
        question_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, question_id, user_id, content):
        # イジられる側のユーザ
        user_id = user_id
        ok = True

        try:
            # イジられる側のユーザを取得
            user = MontageUser.objects.get(id=user_id)
        except ObjectDoesNotExist:
            ok = False

        question = Question.objects.get(id=question_id, user=user)

        impression = Impression.objects.create(
            user=user, question=question, content=content)
        impression.save()
        return CreateImpressionMutation(impression=impression, ok=ok)


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
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        try:
            Impression.objects.filter(id=id).delete()
            ok = True
        except ObjectDoesNotExist:
            ok = False

        return DeleteImpressionMutation(id=id, ok=ok)


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
