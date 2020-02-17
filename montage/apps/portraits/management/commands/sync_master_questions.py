from apps.accounts.models import MontageUser
from apps.portraits.models import Question
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'sync master questions to all users'

    def handle(self, *args, **kwargs):
        users = MontageUser.objects.all()
        questions = Question.objects.all()
        for q in questions:
            for u in users:
                q.user.add(u)
