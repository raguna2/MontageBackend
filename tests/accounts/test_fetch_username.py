import pytest

from montage.schema import schema

from graphene.test import Client
from graphene import Schema


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_fetch_username(snapshot):
    # usernameを取得する
    query = '''users { username }'''

    # schema.pyにある変数 すべてのschemaをまとめている`schema`
    client = Client(schema)

    snapshot.assert_match(client.execute(query))


