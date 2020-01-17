import os
import json
import logging
import http.client

import graphene
from django.contrib.auth import get_user_model, login
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from accounts.models import MontageUser
from auth0 import get_token_auth_header, verify_payload, verify_signature
from jose import jwt
from portraits.models.questions import Question

MGT_CLIENT_ID = os.environ.get('MGT_CLIENT_ID')
MGT_CLIENT_ID_SECRET = os.environ.get('MGT_CLIENT_ID_SECRET')
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
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


class DeleteMontageUserMutation(graphene.Mutation):
    """
    MontageUserの削除
    """
    ok = graphene.Boolean()

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):

        try:
            target = MontageUser.objects.get(username=username)
        except MontageUser.DoesNotExist as e:
            logger.error(e)
            return None

        is_successed = delete_auth0_user(target.identifier_id)

        if is_successed:
            try:
                target.delete()
                ok = True
            except MontageUser.DoesNotExist as e:
                logger.error(e)
                logger.error('存在しないユーザは削除できません')

            logger.info('Djangoデータベースからユーザは削除されました')
        else:
            ok = False
            logger.warning('ユーザ削除に失敗しました.')
        return DeleteMontageUserMutation(ok=ok)


class Mutation(graphene.ObjectType):
    create_user = CreateAuth0User.Field()
    delete_user = DeleteMontageUserMutation.Field()


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

        try:
            user = MontageUser.objects.get(username=username)
        except MontageUser.DoesNotExist as e:
            logger.error(e)
            return None

        return user

    def resolve_users(self, info):
        return MontageUser.objects.all()


def delete_auth0_user(identifier_id: str) -> bool:
    """Auth0のユーザ削除処理

    Parameters
    -------------------
    indentifier_id: str
        Twitterのユーザ識別ID

    Returns
    ---------------
    bool:
        削除が成功したかを表す真偽値


    Notes
    ----------------------
    1. 環境変数からAuth0のマネジメントAPIのアクセストークンを取得するためのID,ID_SECRETを取得

    2. payloadに1で取得したものを含めてアクセストークンを取得(/oauth/token)

    3. 取得したアクセストークンをapiheaderに入れて、`/api/v2/users/{identifier_id}`へ削除処理を投げる

    4. 成功したら、Trueを返す。途中で失敗したら、Falseを返す

    TODOS
    --------------------
    herokuにMGT_CLIENT_ID, MGT_CLIENT_ID_SECRETの環境変数を追加

    """

    # fetch access token for management API
    logger.info('Start to fetch access token for management API')
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = {
        "client_id": MGT_CLIENT_ID,
        "client_secret": MGT_CLIENT_ID_SECRET,
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "grant_type": "client_credentials",
    }
    conn.request(
        "POST",
        "/oauth/token",
        json.dumps(payload),
        {'content-type': "application/json"}
    )

    management_response = conn.getresponse().read().decode("utf-8")
    data = json.loads(management_response)
    logger.debug('data = %s', data)
    if 'access_token' not in data.keys():
        logger.error("fail to fetch access token")
        return False

    logger.info('success fetch access token for management API')

    # access management API and delete Auth0 User
    manage_access_token = data['access_token']
    apiheaders = {'authorization': f"Bearer {manage_access_token}"}

    logger.info('delete auth0 user with management API')
    conn.request("DELETE", f"/api/v2/users/{identifier_id}", headers=apiheaders)
    response = conn.getresponse()

    # 物理削除なので200ではなく204
    if response.status != 204:
        logger.error('Auth0ユーザの削除リクエストに失敗しました.')
        return False

    logger.info('Auth0のDBからユーザの削除が完了しました.')

    return True
