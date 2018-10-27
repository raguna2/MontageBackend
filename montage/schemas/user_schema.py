from montage.apps.accounts.models import MontageUser

import graphene
from graphene_django import DjangoObjectType

from graphene_django.filter import DjangoFilterConnectionField


class UserType(DjangoObjectType):
    """UserType."""
    # sourceと一緒に定義することでpropertyをGQLで取得できる
    as_atsign = graphene.String(source='as_atsign')

    class Meta:
        """Meta."""
        model = MontageUser


class UserSearchType(DjangoObjectType):
    """UserSearchType."""
    as_atsign = graphene.String(source='as_atsign')

    class Meta:
        """Meta."""
        model = MontageUser
        filter_fields = {
            'username': ["icontains"],
        }
        interfaces = (graphene.relay.Node, )

class Mutation(graphene.ObjectType):
    # TODO: Mutationを追加
    pass


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, username=graphene.String())
    users = graphene.List(UserType)
    searched_users = DjangoFilterConnectionField(UserSearchType)

    def resolve_user(self, username, info):
        return MontageUser.objects.get(username=username)

    def resolve_users(self, info):
        return MontageUser.objects.all()
