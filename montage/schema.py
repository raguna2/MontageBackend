from accounts.models import MontageUser
from portraits.models import (Question, Impression)
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


class QuestionType(DjangoObjectType):
    """QuestionType."""
    display_about = graphene.String(source='display_about')

    class Meta:
        """Meta."""
        model = Question


class ImpressionType(DjangoObjectType):
    """ImpressionType."""
    display_content = graphene.String(source='display_content')

    class Meta:
        """Meta."""
        model = Impression


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
    question = graphene.Field(QuestionType, user_id=graphene.Int())
    questions = graphene.List(QuestionType)
    impression = graphene.Field(ImpressionType, question=graphene.String())
    impressions = graphene.List(ImpressionType)

    searched_users = DjangoFilterConnectionField(UserSearchType)

    def resolve_user(self, username, info):
        return MontageUser.objects.get(username=username)

    def resolve_users(self, info):
        return MontageUser.objects.all()

    def resolve_category(self, name, info):
        return Category.objects.get(name=name)

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_question(self, user_id, info):
        return Question.objects.get(user__pk=user_id)

    def resolve_questions(self, info):
        return Question.objects.all()

    def resolve_impression(self, question, info):
        return Impression.objects.get(question=question)

    def resolve_impressions(self, info):
        return Impression.objects.all()


schema = graphene.Schema(query=Query)
