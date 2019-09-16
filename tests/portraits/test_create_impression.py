import logging

import pytest

from montage.schema import schema

from graphene.test import Client
from graphene import Schema


pytestmark = pytest.mark.django_db
logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestCreateImpression:

    def test_it(self, snapshot):
        from ..factories import (
            MontageUserFactory,
            CategoryFactory,
            QuestionFactory,
        )
        user = MontageUserFactory(
            id=104,
            username='RAGUNA104',
            identifier_id='twitter|123456784',
            display_name='kutsumi104'
        )
        logger.info(user)
        user2 = MontageUserFactory(
            id=105,
            username='RAGUNA105',
            identifier_id='twitter|123456785',
            display_name='kutsumi105'
        )
        logger.info(user2)
        category = CategoryFactory(name='サンプルカテゴリ3')
        q_1 = QuestionFactory.create(id=15, about='1?', user=(user, user2), category=category)

        query = '''
        mutation{
          createImpression(content: "この回答が作られます",username: "RAGUNA104", questionId: 15){
            ok
            impression{
              id
              content
            }
          }
        }
        '''

        client = Client(schema)

        snapshot.assert_match(client.execute(query))

