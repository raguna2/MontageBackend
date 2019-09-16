import logging

import graphene
from django.contrib.auth import get_user_model, login
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from accounts.models import MontageUser
from auth0 import get_token_auth_header, verify_payload, verify_signature
from jose import jwt
from portraits.models.questions import Question


logger = logging.getLogger(__name__)


class UserType(DjangoObjectType):
    """UserType."""

    # sourceと一緒に定義することでpropertyをGQLで取得できる

    class Meta:
        """Meta."""
        model = MontageUser


class UserSearchType(DjangoObjectType):
    """
    ユーザ取得用のタイプ

    用途
        1. ユーザIDからユーザを取得する
        2. ユーザ名からユーザを検索する

    検索対象: username
    検索方法: Icontains(含むものを返す)

    IN
    ------
    query{
      searchedUsers(username_Icontains: "a",first: 1){
        edges{
          node{
            username
            asAtsign
            revImpression{
              content
              question{
                about
                category{
                  name
                }
              }
            }
          }
        }
        pageInfo{
          startCursor
          hasNextPage
          hasPreviousPage
        }
      }
    }

    OUT
    --------
    {
      "data": {
        "searchedUsers": {
          "edges": [
            {
              "node": {
                "username": "raguna2",
                "asAtsign": "@raguna2",
                "revImpression": [
                  {
                    "content": "吉田沙保里2",
                    "question": {
                      "about": "好きなスポーツ選手は？",
                      "category": {
                        "name": "スポーツ"
                      }
                    }
                  },
                  {
                    "content": "吉田沙保里",
                    "question": {
                      "about": "好きなスポーツ選手は？",
                      "category": {
                        "name": "スポーツ"
                      }
                    }
                  }
                ]
              }
            }
          ],
          "pageInfo": {
            "startCursor": "YXJyYXljb25uZWN0aW9uOjA=",
            "hasNextPage": true,
            "hasPreviousPage": false
          }
        }
      }
    }
    """
    as_atsign = graphene.String(source='as_atsign')

    class Meta:
        """Meta."""
        model = MontageUser
        filter_fields = {
            'id': ["exact"],
            'username': ["icontains", "startswith"],
        }
        interfaces = (graphene.Node, )
        exclude_fields = ('password')


class UsersUnansweredQuestionsType(DjangoObjectType):
    as_atsign = graphene.String(source='as_atsign')

    class Meta:
        """Meta."""
        model = MontageUser
        filter_fields = {
            'id': ["exact"],
        }
        interfaces = (graphene.Node, )


class UsersAnsweredQuestionsType(DjangoObjectType):
    as_atsign = graphene.String(source='as_atsign')

    class Meta:
        """Meta."""
        model = MontageUser
        filter_fields = {
            'id': ["exact"],
        }
        interfaces = (graphene.Node, )


class CreateAuth0User(graphene.Mutation):
    user = graphene.Field(UserType)

    def mutate(self, info):
        logger.info('create user mutation is start')
        auth_header = info.context.META.get('HTTP_AUTHORIZATION', None)
        if auth_header:
            id_token = get_token_auth_header(auth_header)

        payload = jwt.get_unverified_claims(id_token)

        # exp, iss, audの検証
        validated_payload = verify_payload(payload)

        # signatureの検証
        validated_sign = verify_signature(id_token)

        if validated_payload and validated_sign:
            user_model = get_user_model()
            logger.info('get payload params')
            identifier_id = payload['sub']
            display_name = payload['name']
            username = payload['https://montage.bio/screen_name']
            picture = payload['picture']
            user = None

            if identifier_id and username and display_name:
                user = user_model.objects.create_user(
                    username=username,
                    identifier_id=identifier_id,
                    display_name=display_name,
                    profile_img_url=picture,
                )
                logger.info('created user object')
        else:
            logger.error('検証に失敗')
            user = None

        return CreateAuth0User(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateAuth0User.Field()


class Query(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        username=graphene.String(),
        identifier_id=graphene.String(),
        display_name=graphene.String(),
        picture=graphene.String(),
    )
    users = graphene.List(UserType)
    # ユーザ名での検索用
    searched_users = DjangoFilterConnectionField(UserSearchType)
    # 未回答質問取得用
    users_unanswered_questions = DjangoFilterConnectionField(
        UsersUnansweredQuestionsType)

    def resolve_user(self, info, username):
        return MontageUser.objects.get(username=username)

    def resolve_users(self, info):
        return MontageUser.objects.all()
