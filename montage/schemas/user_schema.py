import os
import json
import re
import requests

from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
from PIL import Image

from accounts.models import MontageUser
from django.contrib.auth import get_user_model
from django.contrib.auth import login

import graphene
from graphene_django import DjangoObjectType
from social_django.utils import load_backend, load_strategy

from graphene_django.filter import DjangoFilterConnectionField
import graphql_jwt
import graphql_social_auth


API_KEY = os.environ.get('SOCIAL_AUTH_TWITTER_KEY')
API_SECRET = os.environ.get('SOCIAL_AUTH_TWITTER_SECRET')



class UserType(DjangoObjectType):
    """UserType."""
    # sourceと一緒に定義することでpropertyをGQLで取得できる
    as_atsign = graphene.String(source='as_atsign')

    class Meta:
        """Meta."""
        model = MontageUser
        exclude_fields = ('password')


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


class CreateAuthenticateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = get_user_model()(
            username=username,
        )
        user.set_password(password)
        user.save()

        return CreateAuthenticateUser(user=user)


class socialAuth(graphene.Mutation):
    """Mutation

    mutation{
      twitterAuth(provider: "twitter", oauthToken: "xxx", oauthVerifier: "xxx") {
        ok
        user{
          username
        }
      }
    }
    """
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    class Arguments:
        provider = graphene.String(required=True)
        oauth_token = graphene.String(required=True)
        oauth_verifier = graphene.String(required=True)

    def mutate(self, info, provider, oauth_token, oauth_verifier):
        ok = True
        # strategyはrequestのデータやsessionの情報を扱うためのもの
        request = info.context
        strategy = load_strategy(request)
        backend = load_backend(
            strategy,
            provider,
            redirect_uri='/complete/twitter/'
        )
        consumer_key = API_KEY
        consumer_secret = API_SECRET
        twitter = OAuth1Session(
            consumer_key,
            consumer_secret,
            oauth_token,
            oauth_verifier,
        )

        response = twitter.post(
            'https://api.twitter.com/oauth/access_token/',
            params={'oauth_verifier': oauth_verifier}
        )
        access_token = dict(parse_qsl(response.content.decode("utf-8")))

        try:
            user = backend.do_auth(access_token)
        except BaseException as e:
            print(e)
            ok = False

        if user:
            login(request, user)
        else:
            ok = False

        return socialAuth(ok, user)


class Mutation(graphene.ObjectType):
    create_user = CreateAuthenticateUser.Field()
    twitter_auth = socialAuth.Field()



class Query(graphene.ObjectType):
    user = graphene.Field(UserType, username=graphene.String())
    users = graphene.List(UserType)
    # ユーザ名での検索用
    searched_users = DjangoFilterConnectionField(UserSearchType)
    # 未回答質問取得用
    users_unanswered_questions = DjangoFilterConnectionField(
        UsersUnansweredQuestionsType)
    me = graphene.Field(UserType)
    tokens = graphene.String()
    tokens2 = graphene.String()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')

        return user

    def resolve_user(self, info, username):
        return MontageUser.objects.get(username=username)

    def resolve_users(self, info):
        return MontageUser.objects.all()

    def resolve_tokens(self, info):

        CALLBACK_URL = 'http://127.0.0.1:8080/auth/twitter/callback/'
        twitter_api = OAuth1Session(API_KEY, API_SECRET)
        response = twitter_api.post(
            'https://api.twitter.com/oauth/request_token',
            params={
                'oauth_callback': CALLBACK_URL
            }
        )

        return response.text

    def resolve_tokens2(self, info):
        twitter_api = OAuth1Session(API_KEY, API_SECRET)

        # user情報を取得する場合
        username = 'RAGUNA2'
        url = f"https://api.twitter.com/1.1/users/show.json?screen_name={username}"
        response = twitter_api.get(url)
        res = json.loads(response.text)

        # 画像を取得する場合
        base_image_url = res['profile_image_url'].rsplit('_', 1)[0]
        image_url_square = base_image_url + '_400x400'
        r = requests.get(image_url_square, stream=True)
        filename = f"scale.jpeg"
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)

        img = Image.open(filename)
        img.save('./scale.jpeg')

        # 名前を取得する場合
        name = res['name']
        return res
