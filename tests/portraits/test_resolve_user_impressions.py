import pytest

from montage.schema import schema

from graphene.test import Client
from graphene import Schema


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestResolveUserImpressions:

    def test_it(self, snapshot):
        from ..factories import (
            MontageUserFactory,
            CategoryFactory,
            QuestionFactory,
            ImpressionFactory
        )
        user = MontageUserFactory(
            id=100,
            username='RAGUNA100',
            identifier_id='twitter|123456789',
            display_name='kutsumi100'
        )
        user2 = MontageUserFactory(
            id=101,
            username='RAGUNA101',
            identifier_id='twitter|123456781',
            display_name='kutsumi101'
        )
        category = CategoryFactory(name='サンプルカテゴリ')
        q_1 = QuestionFactory.create(about='1?', user=(user, user2), category=category)
        ImpressionFactory(content='この回答は表示されます1', user=user, question=q_1)

        QuestionFactory(about='2?', user=(user, user2), category=category)

        q_3 = QuestionFactory(about='3?', user=(user, user2), category=category)
        ImpressionFactory(content='この回答は表示されません', user=user, question=q_3)
        ImpressionFactory(content='この回答は表示されません', user=user, question=q_3)
        ImpressionFactory(content='この回答は表示されます2', user=user, question=q_3)

        QuestionFactory(about='4?', user=(user, user2), category=category)

        q_5 = QuestionFactory(about='5?', user=(user, user2), category=category)
        ImpressionFactory(content='この回答は表示されません', user=user, question=q_5)
        ImpressionFactory(content='この回答は表示されます3', user=user, question=q_5)

        query = '''query{ userImpressions(username: "RAGUNA100", page: 0, size: 5){ id content question{ id about category{ id name } } } }'''
        client = Client(schema)

        snapshot.assert_match(client.execute(query))
