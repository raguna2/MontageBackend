from montage.apps.accounts.models import MontageUser
from montage.apps.portraits.models import (Question, Impression)
from montage.apps.categories.models import Category

import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .schemas.category_schema import (CategoryType, CreateCategoryMutation,
                                      UpdateCategoryMutation, DeleteCategoryMutation)
from .schemas.user_schema import (UserType, UserSearchType)
from .schemas.impression_schema import ImpressionType
from .schemas.question_schema import QuestionType


class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()


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


schema = graphene.Schema(query=Query, mutation=Mutation)
