from django.conf import settings
from django.db import models


class Friendship(models.Model):
    """
    ユーザの関連人物を示すモデル

    wikiの関連人物のようなイメージ

    relate_from:
        関係をはっている人

    relate_to:
        関係づけられた人
    """
    relate_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='friendship_from',
        on_delete=models.CASCADE
    )

    relate_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='friendship_to',
        on_delete=models.CASCADE
    )
