from django.shortcuts import resolve_url
from django.test import TestCase


class ViewTest(TestCase):
    def test_mainview(self):
        response = self.client.get(resolve_url('accounts:main'))

        self.assertTemplateUsed(response, 'templates/user.html')
        assert response.status_code == 200
