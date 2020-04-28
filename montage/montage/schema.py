from apps.accounts.schemas import Mutation as user_mute
from apps.accounts.schemas import Query as user_query
from apps.categories.schemas import Mutation as category_mute
from apps.categories.schemas import Query as category_query
from apps.portraits.impression_schema import Mutation as impression_mute
from apps.portraits.impression_schema import Query as impression_query
from apps.portraits.question_schema import Mutation as question_mute
from apps.portraits.question_schema import Query as question_query
import graphene
from graphene_django.debug import DjangoDebug


class Mutation(
        user_mute,
        category_mute,
        impression_mute,
        question_mute,
        graphene.ObjectType
):
    pass


class Query(
        user_query,
        category_query,
        impression_query,
        question_query,
        graphene.ObjectType
):
    # デバッグでSQL確認する用
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
