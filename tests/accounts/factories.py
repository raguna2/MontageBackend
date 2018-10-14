import factory

from datetime import datetime
from accounts.models import MontageUser


class MontageUserFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda o: o + 1)
    username = 'raguna2'
    is_staff = True
    is_superuser = True
    display_name = 'くつみ'
    email = factory.lazy_attribute(lambda o: f'{o.username}@gmail.com')

    class Meta:
        model = MontageUser
