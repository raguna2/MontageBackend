from accounts.models import MontageUser

import graphene
from graphene_django import DjangoObjectType


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
