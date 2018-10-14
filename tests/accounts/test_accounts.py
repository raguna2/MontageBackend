import pytest


@pytest.mark.django_db
class TestMainView:

    @pytest.fixture
    def target(self, client):
        return client.get

    @pytest.mark.parametrize(
        'url,expected', [
            ('/', 200,),
            ('/admin/login/?next=/admin/', 200,),
            # ('/gql/', 200,),
        ]
    )
    def test_it(self, target, url, expected):
        # arrange
        from .factories import MontageUserFactory
        MontageUserFactory()

        # act
        response = target(url)
        actual = response.status_code

        # assert
        assert actual == expected
