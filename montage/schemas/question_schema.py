from portraits.models import Question

import graphene
from graphene_django import DjangoObjectType


class QuestionType(DjangoObjectType):
    """QuestionType."""
    display_about = graphene.String(source='display_about')

    class Meta:
        """Meta."""
        model = Question