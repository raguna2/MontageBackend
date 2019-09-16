import logging

from django.core.exceptions import ObjectDoesNotExist

from accounts.models import MontageUser
from friendships.models import Friendship
from categories.models import Category

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


logger = logging.getLogger(__name__)


class FriendshipType(DjangoObjectType):
    """FriendshipType."""

    class Meta:
        """Meta."""
        model = Friendship
        filter_fields = {
            'relate_from__id': ["exact"],
        }
        interfaces = (graphene.Node, )


class CreateFriendshipMutation(graphene.Mutation):
    """
    Friendshipの作成（ログイン必須）

    IN
    -------
    mutation{
      createFriendship(relateTo_Id: 2){
        ok
        friendship{
          relateFrom{
            identifier_id
          }
          relateTo{
            identifier_id
          }
        }
      }
    }

    OUT
    -----
    {
      "data": {
        "createFriendship": {
          "ok": true,
          "friendship": {
            "relateFrom": {
              "identifier_id": "twitter|17000000"
            },
            "relateTo": {
              "identifier_id": "twitter|17000001"
            }
          }
        }
      }
    }
    """
    friendship = graphene.Field(FriendshipType)
    ok = graphene.Boolean()

    class Input:
        relate_to__id = graphene.Int()

    def mutate(self, info, **input):

        if info.context.user.is_anonymous:
            logger.error('ユーザがanonymousです.')
            raise Exception('Not logged!')

        try:
            relate_to = MontageUser.objects.get(
                id=input.get('relate_to__id')
            )
            friendship = Friendship.objects.create(
                relate_from=info.context.user, relate_to=relate_to)
            friendship.save()
            ok = True
        except ObjectDoesNotExist as e:
            logger.error(e)
            ok = False

        return CreateFriendshipMutation(friendship=friendship, ok=ok)


class DeleteFriendshipMutation(graphene.Mutation):
    """
    Friendshipの削除

    IN
    -----
    mutation{
      deleteFriendship(id: 1){
        ok
      }
    }

    OUT
    -------
    {
      "data": {
        "deleteFriendship": {
          "ok": true
        }
      }
    }
    """
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, **input):
        friendship = Friendship.objects.filter(id=input.get('id'))
        try:
            friendship.delete()
            ok = True
        except ObjectDoesNotExist as e:
            logger.error('存在しないオブジェクトは削除できません')
            logger.error(e)
            ok = False

        return DeleteFriendshipMutation(ok=ok)


class Mutation(graphene.ObjectType):
    create_friendship = CreateFriendshipMutation.Field()
    delete_friendship = DeleteFriendshipMutation.Field()


class Query(graphene.ObjectType):
    """
    Query

    IN
    ------
    query{
      friendship(relateFrom_Id: 1){
        edges{
          node{
            relateFrom{
              identifier_id
            }
            relateTo{
              identifier_id
            }
          }
        }
      }
    }
    """
    friendship = DjangoFilterConnectionField(FriendshipType)
