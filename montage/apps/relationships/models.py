from django.db import models

from montage.settings.common import AUTH_USER_MODEL


class Relationship(models.Model):
    """
    フォロー機能の関係を表す中間モデル

    following:
        フォローする人

    followed:
        フォローされた人
    """
    following = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='follows',
        on_delete=models.CASCADE
    )

    followed = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='followers',
        on_delete=models.CASCADE
    )
