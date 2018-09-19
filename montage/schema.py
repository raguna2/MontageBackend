import graphene
from accounts.models import MontageUser
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


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, username=graphene.String())
    users = graphene.List(UserType)
    searched_users = DjangoFilterConnectionField(UserSearchType)

    @graphene.resolve_only_args
    def resolve_user(self, username):
        return MontageUser.objects.get(username=username)

    @graphene.resolve_only_args
    def resolve_users(self):
        return MontageUser.objects.all()


schema = graphene.Schema(query=Query)
