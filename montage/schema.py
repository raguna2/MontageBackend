import graphene
from montage.schemas import (
    category_mute,
    category_query,
    friendship_mute,
    friendship_query,
    impression_mute,
    impression_query,
    question_mute,
    question_query,
    relate_mute,
    relate_query,
    user_mute,
    user_query
)


class Mutation(user_mute, category_mute, impression_mute,
               question_mute, relate_mute, friendship_mute,
               graphene.ObjectType):
    pass


class Query(user_query, category_query, impression_query,
            question_query, relate_query, friendship_query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
