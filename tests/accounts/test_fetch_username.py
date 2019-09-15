import pytest
from graphene import Schema
from graphene.test import Client

from montage.schema import schema

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestFetchUsers:
    @pytest.mark.parametrize('user_data', [
        [
            {
                'id': 1,
                'username': 'RAGUNA1',
                'identifier_id': 'admin|0000001',
                'display_name': 'ユーザ1',
            },
            {
                'id': 2,
                'username': 'RAGUNA2',
                'identifier_id': 'admin|0000002',
                'display_name': 'ユーザ2',
            },
            {
                'id': 3,
                'username': 'RAGUNA3',
                'identifier_id': 'admin|0000003',
                'display_name': 'ユーザ3',
            },
            {
                'id': 4,
                'username': 'RAGUNA4',
                'identifier_id': 'admin|0000004',
                'display_name': 'ユーザ4',
            },
        ]
    ])
    def test_it(self, snapshot, user_data):
        from ..factories import MontageUserFactory
        for data in user_data:
            MontageUserFactory(
                id=data['id'],
                username=data['username'],
                identifier_id=data['identifier_id'],
                display_name=data['display_name']
            )
        query = '''query{users { id username identifierId displayName}}'''

        # schema.pyにある変数 すべてのschemaをまとめている`schema`
        client = Client(schema)

        snapshot.assert_match(client.execute(query))
