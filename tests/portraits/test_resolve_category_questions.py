import pytest

from montage.schema import schema

from graphene.test import Client
from graphene import Schema


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestResolveCategoryQuestions:

    def test_it(self, snapshot):
        from ..factories import (
            MontageUserFactory,
            CategoryFactory,
            QuestionFactory,
            ImpressionFactory
        )
        user = MontageUserFactory(
            id=102,
            username='RAGUNA102',
            identifier_id='twitter|123456782',
            display_name='kutsumi102'
        )
        user2 = MontageUserFactory(
            id=103,
            username='RAGUNA103',
            identifier_id='twitter|123456783',
            display_name='kutsumi103'
        )
        category = CategoryFactory(name='サンプルカテゴリ')
        q_1 = QuestionFactory.create(about='この質問は表示されません1', user=(user, user2), category=category)
        q_3 = QuestionFactory(about='この質問は表示されません2', user=(user, user2), category=category)
        q_5 = QuestionFactory(about='この回答は表示されません3', user=(user, user2), category=category)

        QuestionFactory(about='この質問は表示されます1', user=(user, user2), category=category)
        QuestionFactory(about='この質問は表示されます2', user=(user, user2), category=category)

        ImpressionFactory(user=user, question=q_1)
        ImpressionFactory(user=user, question=q_3)
        ImpressionFactory(user=user, question=q_5)

        query = '''query{categoryQuestions(userId:102,categoryName:"サンプルカテゴリ",page: 0,size:4){id about}}'''

        # expected: 2, 4
        client = Client(schema)

        snapshot.assert_match(client.execute(query))
