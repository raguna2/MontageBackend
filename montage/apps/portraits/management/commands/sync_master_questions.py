from django.core.management.base import BaseCommand
from django.utils import timezone
from portraits.models.questions import Question
from accounts.models import MontageUser


class Command(BaseCommand):
    help = 'sync master questions to all users'

    def handle(self, *args, **kwargs):
        users = MontageUser.objects.all()
        questions = Question.objects.all()
        for q in questions:
            for u in users:
                q.user.add(u)
