from portraits.models import Impression

import graphene
from graphene_django import DjangoObjectType


class ImpressionType(DjangoObjectType):
    """ImpressionType."""
    display_content = graphene.String(source='display_content')

    class Meta:
        """Meta."""
        model = Impression