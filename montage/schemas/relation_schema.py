from django.core.exceptions import ObjectDoesNotExist

from accounts.models import MontageUser
from relationships.models import Relationship
from categories.models import Category

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from montage.apps.logging import logger_e


class RelationshipType(DjangoObjectType):
    """RelationshipType."""

    class Meta:
        """Meta."""
        model = Relationship
        filter_fields = {
            'following_id': ["exact"],
        }
        interfaces = (graphene.Node, )


class CreateRelationshipMutation(graphene.Mutation):
    """
    Relationshipの作成

    IN
    =-------
    mutation{
      createRelation(followingUserId: 1, followedUserId: 4){
        relation{
          following{
            id
            username
            asAtsign
          }
          followed{
            id
            username
            asAtsign
          }
        }
        ok
      }
    }

    OUT
    ------
    {
      "data": {
        "createRelation": {
          "relation": {
            "following": {
              "id": "VXNlclNlYXJjaFR5cGU6MQ==",
              "username": "raguna2",
              "asAtsign": "@raguna2"
            },
            "followed": {
              "id": "VXNlclNlYXJjaFR5cGU6NA==",
              "username": "kai",
              "asAtsign": "@kai"
            }
          },
          "ok": true
        }
      }
    }

    Notes
    --------
    info.context.userはログインしているユーザ情報なので、
    ログインしない状態でフォローしてもAnonymousUserが渡されてだめ
    ------
    """
    relation = graphene.Field(RelationshipType)
    ok = graphene.Boolean()

    class Input:
        following_user_id = graphene.Int()
        followed_user_id = graphene.Int()

    def mutate(self, info, **input):
        try:
            followed = MontageUser.objects.get(
                id=input.get('followed_user_id')
            )
            relation = Relationship.objects.create(
                following=info.context.user, followed=followed
            )
            relation.save()
            ok = True
        except ObjectDoesNotExist:
            ok = False

        return CreateRelationshipMutation(relation=relation, ok=ok)


class DeleteRelationshipMutation(graphene.Mutation):
    """
    Relationshipの削除

    IN
    -----
    mutation{
      deleteRelation(id: 4){
        ok
      }
    }

    OUT
    -------
    {
      "data": {
        "deleteRelation": {
          "ok": true
        }
      }
    }
    """
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, **input):
        relation = Relationship.objects.filter(id=input.get('id'))
        try:
            relation.delete()
            ok = True
        except ObjectDoesNotExist:
            logger_e.error('存在しないオブジェクトは削除できません')
            ok = False

        return DeleteRelationshipMutation(ok=ok)


class Mutation(graphene.ObjectType):
    create_relation = CreateRelationshipMutation.Field()
    delete_relation = DeleteRelationshipMutation.Field()


class Query(graphene.ObjectType):
    """
    フォローしている側のユーザIDを指定して友達一覧を取得する

    IN
    -------
    query{
      relations(followingId: 1){
        edges{
          node{
            following{
              username
            }
            followed{
              username
            }
          }
        }
      }
    }

    OUT
    ------
    {
      "data": {
        "relations": {
          "edges": [
            {
              "node": {
                "following": {
                  "username": "montage"
                },
                "followed": {
                  "username": "kai"
                }
              }
            },
        }
    }
    """
    relations = DjangoFilterConnectionField(RelationshipType)
