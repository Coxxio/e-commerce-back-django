from django.urls import reverse

from rest_framework import status

from ..test_setup import TestSetupClient


class UsersClientAPITestCase(TestSetupClient):

    def test_00_delete_user_self(self):
        url = reverse(self.url_destroy_self)
        response = self.client.delete(url)

        # Tests
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
