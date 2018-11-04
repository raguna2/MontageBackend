from django.db import models
from accounts.models import MontageUser
from portraits.models import Impression


class Comment(models.Model):
    """docstring for Comment."""
    body = models.TextField("コメント本文", max_length=200)
    impression = models.ForeignKey(
        Impression,
        on_delete=models.PROTECT,
        related_name="comments",
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    user = models.ForeignKey(
        MontageUser,
        on_delete=models.PROTECT,
        related_name="comments"
    )
    is_parent = models.BooleanField()
