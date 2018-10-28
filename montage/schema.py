import graphene

# MontageUser
from montage.schemas.user_schema import (
    UserType, Mutation as user_mute, Query as user_query)

# Category
from montage.schemas.category_schema import (
    CategoryType, Mutation as category_mute, Query as category_query)

# Impression
from montage.schemas.impression_schema import (
    ImpressionType, Query as impression_query, Mutation as impression_mute)

# Question
from montage.schemas.question_schema import (
    QuestionType, Query as question_query, Mutation as question_mute)


class Mutation(user_mute, category_mute, impression_mute,
               question_mute, graphene.ObjectType):
    pass


class Query(user_query, category_query, impression_query,
            question_query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
