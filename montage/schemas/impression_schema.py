import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from accounts.models import MontageUser
from portraits.models.questions import Question
from portraits.models.impressions import Impression

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


logger = logging.getLogger(__name__)


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
      createImpression(content: "ワロタ", username: "RAGUNA2", questionId: 11){
        ok
        impression{
          id
          content
          postedAt
        }
      }
    }

    OUT
    ------------
    {
      "data": {
        "createImpression": {
          "ok": true,
          "impression": {
            "id": "4",
            "content": "ワロタ",
            "postedAt": "2019-09-08T09:41:24.208806+00:00"
          }
        }
      }
    }
    """
    impression = graphene.Field(ImpressionType)
    ok = graphene.Boolean()

    class Input:
        question_id = graphene.Int(required=True)
        username = graphene.String(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, question_id, username, content):
        ok = True

        try:
            user = MontageUser.objects.get(username=username)
        except ObjectDoesNotExist as e:
            logger.error(e)
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
        except ObjectDoesNotExist as e:
            logger.error(e)
            ok = False

        return DeleteImpressionMutation(id=id, ok=ok)


class Mutation(graphene.ObjectType):
    create_impression = CreateImpressionMutation.Field()
    delete_impression = DeleteImpressionMutation.Field()


class Query(graphene.ObjectType):
    # 任意の質問に対する回答の一覧
    impression = graphene.Field(ImpressionType, question=graphene.String())

    # すべての回答
    impressions = graphene.List(ImpressionType)

    # ユーザ毎の回答済み一覧
    user_impressions = graphene.List(
        ImpressionType,
        username=graphene.String(),
        page=graphene.Int(),
        size=graphene.Int(),
    )

    def resolve_impression(self, info, question):
        return Impression.objects.get(question=question)

    def resolve_impressions(self, info):
        return Impression.objects.all()

    def resolve_user_impressions(self, info, username, page, size):
        """ユーザ毎の回答済みimpressionsを取得するときのクエリ結果

        Parameters
        -----------
        username: str
            ユーザ名

        page: int
            ページ数

        size: int
            一度に何個取得するか

        Notes
        ----------
        クエリと取得結果はsnapshotテストを参照

        """
        user = MontageUser.objects.get(username=username)
        # 回答がすでにあるquestionを取得
        impressed_q = Question.objects.filter(
            user=user,
            rev_impression__isnull=False
        ).distinct()

        # 回答がすでにある質問ごとに最新のimpressionを取得
        all_imp = [q.rev_impression.latest('posted_at') for q in impressed_q]

        # ページ番号と取得数を指定し、その数にあった分のimpressionを返す
        start = page * size if page > 0 else 0
        end = size + page * size if page > 0 else size
        return all_imp[start:end]
