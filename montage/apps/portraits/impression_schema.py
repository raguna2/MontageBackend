import logging

from apps.accounts.models import MontageUser
from apps.montage_core.utils import upload_base64_img_to_cloudinary
from apps.portraits.images import create_ogp_share_image
from apps.portraits.models import Impression, Question
from django.core.exceptions import ObjectDoesNotExist
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

logger = logging.getLogger(__name__)


class ImpressionType(DjangoObjectType):
    """ImpressionType."""

    class Meta:
        """Meta."""
        model = Impression


class UserAnswersType(graphene.ObjectType):
    """あるユーザの質問に紐づく回答のType"""
    id = graphene.Int()
    content = graphene.String()
    createrUserName = graphene.String()
    posted_at = graphene.String()
    impression_img_url = graphene.String()


class QuestionAndAnswersType(graphene.ObjectType):
    """あるユーザに紐づく質問とその質問に紐づく回答の一覧を表すType"""
    id = graphene.Int()
    about = graphene.String()
    items = graphene.List(UserAnswersType)


class CreateImpressionMutation(graphene.Mutation):
    """
    Impressionの作成

    Notes
    ---------------
    入出力仕様はsnapshotテストを参考

    """
    impression = graphene.Field(ImpressionType)
    ok = graphene.Boolean()

    class Input:
        question_id = graphene.Int(required=True)
        username = graphene.String(required=True)
        content = graphene.String(required=True)
        auth_username = graphene.String(required=True)

    def mutate(self, info, question_id, username, content, auth_username):
        ok = True

        try:
            user = MontageUser.objects.get(username=username)
        except ObjectDoesNotExist:
            logger.exception('Montage User does not exists.')
            raise GraphQLError('target User does not exists. username = %s', username)

        logger.debug('start to get target question.')
        question = Question.objects.get(id=question_id)

        try:
            creater = MontageUser.objects.get(username=auth_username)
        except ObjectDoesNotExist:
            logger.exception('Montage User of creating impression does not exists.')
            raise GraphQLError('creater User does not exists. username = %s', username)

        # OGP用のシェア画像作成&Cloudinaryへのアップロード処理
        logger.info('start create share image.')
        uploaded_url = ""
        share_img_base64 = create_ogp_share_image(user.profile_img_url, question.about, content)

        if not share_img_base64:
            logger.info('failed to create share image.')
        else:
            logger.info('start upload share image to cloudinary.')
            share_img_uri = f"data:image/png;base64,{share_img_base64}"
            uploaded_url = upload_base64_img_to_cloudinary(share_img_uri)
            if not uploaded_url:
                logger.info('failed to upload shared image to cloudinary.')

        impression = Impression.objects.create(
            user=user,
            question=question,
            content=content,
            created_by=creater,
            impression_img_url=uploaded_url,
        )
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
        delete_impression_id = graphene.Int()

    def mutate(self, info, delete_impression_id):
        try:
            Impression.objects.filter(id=delete_impression_id).delete()
            ok = True
        except ObjectDoesNotExist as e:
            logger.error(e)
            ok = False

        return DeleteImpressionMutation(ok=ok)


class Mutation(graphene.ObjectType):
    create_impression = CreateImpressionMutation.Field()
    delete_impression = DeleteImpressionMutation.Field()


class Query(graphene.ObjectType):
    # 任意の質問に対する回答の一覧
    impression = graphene.Field(ImpressionType, question=graphene.String())

    # すべての回答
    impressions = graphene.List(ImpressionType)

    # プロフィールに表示する最新の質問と回答一覧(回答は質問に紐づくすべての回答)
    user_impressions = graphene.List(
        QuestionAndAnswersType,
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
        user_exists = MontageUser.objects.filter(username=username).exists()

        if not user_exists:
            logger.info('user does not exists')
            raise GraphQLError('User does not exists. username = %s', username)

        impressed_q = Impression.objects.select_related(
            'question'
        ).filter(
            user__username=username
        ).order_by('-posted_at')
        if not impressed_q:
            logger.debug('回答済みの質問はありませんでした')
            return []

        impressed_q_ids = list(set([i.question.id for i in impressed_q]))

        # ページ番号と取得数を指定し、その数にあった分のimpressionを返す
        start = page * size if page > 0 else 0
        end = size + page * size if page > 0 else size

        result = []
        # 回答のある質問一覧
        questions = Question.objects.filter(
            user__username=username,
            id__in=impressed_q_ids,
        )[start:end]

        for q in questions:
            # 質問毎の回答一覧をリストとして内包表記で生成
            items = [
                UserAnswersType(
                    id=i.id,
                    content=i.content,
                    createrUserName=i.created_by.username,
                    posted_at=i.posted_at,
                    impression_img_url=i.impression_img_url,
                )
                for i in impressed_q if i.question.id == q.id
            ]
            qa = QuestionAndAnswersType(
                id=q.id,
                about=q.about,
                items=items,
            )
            result.append(qa)

        return result
