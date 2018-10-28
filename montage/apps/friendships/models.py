from django.db import models

from montage.settings.common import AUTH_USER_MODEL


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
        AUTH_USER_MODEL,
        related_name='friendship_from',
        on_delete=models.CASCADE
    )

    relate_to = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='friendship_to',
        on_delete=models.CASCADE
    )
