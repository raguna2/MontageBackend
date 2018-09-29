from accounts.models import MontageUser
from portraits.models import (Impression, Hearsay)
from categories.models import Category

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


class ImpressionType(DjangoObjectType):
    """ImpressionType."""
    display_about = graphene.String(source='display_about')

    class Meta:
        """Meta."""
        model = Impression


class HearsayType(DjangoObjectType):
    """HearsayType."""
    display_content = graphene.String(source='display_content')

    class Meta:
        """Meta."""
        model = Hearsay


class CategoryType(DjangoObjectType):
    """CategoryType"""
    class Meta:
        """Meta."""
        model = Category


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
    category = graphene.Field(CategoryType, name=graphene.String())
    categories = graphene.List(CategoryType)
    impression = graphene.Field(ImpressionType, user_id=graphene.Int())
    impressions = graphene.List(ImpressionType)
    hearsay = graphene.Field(HearsayType, impression=graphene.String())
    hearsays = graphene.List(HearsayType)

    searched_users = DjangoFilterConnectionField(UserSearchType)

    @graphene.resolve_only_args
    def resolve_user(self, username):
        return MontageUser.objects.get(username=username)

    @graphene.resolve_only_args
    def resolve_users(self):
        return MontageUser.objects.all()

    @graphene.resolve_only_args
    def resolve_category(self, name):
        return Category.objects.get(name=name)

    @graphene.resolve_only_args
    def resolve_categories(self):
        return Category.objects.all()

    @graphene.resolve_only_args
    def resolve_impression(self, user_id):
        return Impression.objects.get(user__pk=user_id)

    @graphene.resolve_only_args
    def resolve_impressions(self):
        return Impression.objects.all()

    @graphene.resolve_only_args
    def resolve_hearsay(self, impression):
        return Hearsay.objects.get(impression=impression)

    @graphene.resolve_only_args
    def resolve_hearsays(self):
        return Hearsay.objects.all()


schema = graphene.Schema(query=Query)
