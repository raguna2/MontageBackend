from accounts.models import MontageUser
from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

from graphene_django.filter import DjangoFilterConnectionField
import graphql_social_auth



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


class Mutation(graphene.ObjectType):
    """Mutation

    IN(https://api.twitter.com/oauth/authorizeに対してリクエスト)
    ----------
    mutation{
       socialAuth(provider: "twitter",accessToken: "twitterのアクセストークン"){
          social{
              uid
              user{
                  username
                  asAtsign
              }
          }
       }
    }
    """
    create_user = CreateAuthenticateUser.Field()
    social_auth = graphql_social_auth.SocialAuth.Field()


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, username=graphene.String())
    users = graphene.List(UserType)
    # ユーザ名での検索用
    searched_users = DjangoFilterConnectionField(UserSearchType)
    # 未回答質問取得用
    users_unanswered_questions = DjangoFilterConnectionField(
        UsersUnansweredQuestionsType)
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')

        return user

    def resolve_user(self, info, username):
        return MontageUser.objects.get(username=username)

    def resolve_users(self, info):
        return MontageUser.objects.all()
