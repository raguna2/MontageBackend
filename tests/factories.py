from datetime import datetime

from django.utils import timezone

import factory
import factory.fuzzy
from accounts.models import MontageUser
from categories.models import Category
from portraits.models import impressions, questions


class MontageUserFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda o: o + 1)
    username = 'raguna2'
    identifier_id = factory.Sequence(lambda i: 'twitter|{:08d}'.format(i))
    is_staff = True
    is_superuser = True
    display_name = 'くつみ'

    class Meta:
        model = MontageUser


class CategoryFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda o: o + 1)
    name = factory.Sequence(lambda i: 'カテゴリ{:01d}'.format(i))
    description = factory.Sequence(lambda i: 'カテゴリの説明{:01d}'.format(i))

    class Meta:
        model = Category


class QuestionFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda o: o + 1)
    about = factory.Sequence(lambda i: '質問{:04d}'.format(i))
    category = factory.SubFactory(CategoryFactory)
    appeared_at = factory.fuzzy.FuzzyDateTime(timezone.now())

    class Meta:
        model = questions.Question

    @factory.post_generation
    def user(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for u in extracted:
                self.user.add(u)


class ImpressionFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda o: o + 1)
    content = factory.Sequence(lambda i: '回答{:04d}'.format(i))
    posted_at = factory.fuzzy.FuzzyDateTime(timezone.now())

    class Meta:
        model = impressions.Impression
