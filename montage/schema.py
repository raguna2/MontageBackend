import graphene
import graphql_jwt

from montage.schemas import (
    user_mute, user_query,
    impression_mute, impression_query,
    question_mute, question_query,
    category_mute, category_query,
    relate_mute, relate_query,
    friendship_mute, friendship_query,
)


class Mutation(user_mute, category_mute, impression_mute,
               question_mute, relate_mute, friendship_mute,
               graphene.ObjectType):
    """
    ログインのためのトークン取得方法

    IN
    -------
    mutation{
      tokenAuth(username: "raguna923", password: "password"){
        token
      }
    }

    OUT
    ------
    {
      "data": {
        "tokenAuth": {
          "token": "ここにトークンが入る"
        }
      }
    }

    IN(verifyTokenで有効期限が確認可能)
    ----------
    mutation{
      verifyToken(token: ""
        payload
      }
    }

    OUT
    ----------
    {
      "data": {
        "verifyToken": {
          "payload": {
            "username": "raguna923",
            "exp": 1541312953,
            "origIat": 1541312653
          }
        }
      }
    }


    """
    # JSON Web tokenを取得するためのトークン
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # トークンが有効であることを確認する値
    verify_token = graphql_jwt.Verify.Field()
    # トークンが有効期限になる前に新しいものを取得するためのトークン
    refresh_token = graphql_jwt.Refresh.Field()


class Query(user_query, category_query, impression_query,
            question_query, relate_query, friendship_query,
            graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
