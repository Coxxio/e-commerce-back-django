from urllib import response
from ..test_setup import TestSetup

from django.urls import reverse

from rest_framework import status


class UsersAPITestCase(TestSetup):

    def data_success_category_JSON(self):
        return {
            "name": "Zapatos",
        }

    def data_fail_category_JSON(self):
        return {
            "name": "Ropa de dama",
        }

    def data_success_update_category_JSON(self):
        return {
            "name": "Camisas",
        }

    def test_00_get_all_category(self):
        url = reverse(self.routes['url_category_list_create'])
        response = self.client.get(url, format='json')
        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Method invalid'
        )

    def test_01_post_success_category(self):
        url = reverse(self.routes['url_category_list_create'])
        response = self.client.post(
            url,
            self.data_success_category_JSON(),
            format='json'
        )

        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            'Method invalid'
        )

    def test_02_post_fail_category(self):
        url = reverse(self.routes['url_category_list_create'])
        res = self.client.post(
            url,
            self.data_fail_category_JSON(),
            format='json'
        )

        # Tests
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST,
            'Method invalid'
        )

        self.assertEqual(
            res.data['errors']['name'][0],
            "Category already registered"
        )

    def test_03_update_category(self):
        url = reverse(self.routes['url_category_retrieve_update'],
                      kwargs={'pk': self.category_id_test})
        res = self.client.put(
            url,
            self.data_success_update_category_JSON(),
            format='json'
        )

        # Tests
        self.assertEqual(
            res.status_code,
            status.HTTP_202_ACCEPTED,
            'Method invalid'
        )

        self.assertEqual(
            res.data['data']['name'],
            'Camisas'
        )

    def test_04_update_repeat_name_category(self):
        url = reverse(self.routes['url_category_retrieve_update'],
                      kwargs={'pk': self.category_id_test_2})
        res = self.client.put(
            url,
            self.data_fail_category_JSON(),
            format='json'
        )

        # Tests
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST,
            'Method invalid'
        )

        self.assertEqual(
            res.data['errors']['name'][0],
            'Category already registered'
        )

    def test_05_get_one_category(self):
        url = reverse(self.routes['url_category_list_create'])
        res = self.client.post(
            url,
            self.data_success_category_JSON(),
            format='json'
        )
        url = reverse(self.routes['url_category_retrieve_update'],
                      kwargs={'pk': res.data['data']['id']})
        res = self.client.get(
            url
        )
        # Tests
        self.assertEqual(
            res.status_code,
            status.HTTP_200_OK,
            'Method invalid'
        )

        self.assertEqual(
            res.data['data']['name'],
            'Zapatos'
        )

    def test_06_delete_category(self):
        url = reverse(self.routes['url_category_list_create'])
        res = self.client.post(
            url,
            self.data_success_category_JSON(),
            format='json'
        )
        url = reverse(self.routes['url_category_retrieve_update'],
                      kwargs={'pk': res.data['data']['id']})
        res = self.client.delete(
            url
        )
        # Tests
        self.assertEqual(
            res.status_code,
            status.HTTP_202_ACCEPTED,
            'Method invalid'
        )
