from ..test_setup import TestSetup

from django.urls import reverse

from rest_framework import status


class ProductsAPITestCase(TestSetup):

    def data_success_product_JSON(self):
        return {
            "name": "Camisa test",
            "description": "descripcion test",
            "stock": "10",
            "price": "10.0",
            "category": "de0e6f32-bc71-4402-a595-516e7bd4db0c",
        }
        
    def test_00_get_all_products(self):
        url = reverse(self.routes['url_list_products'])
        response = self.client.get(url, format="json")
        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Method invalid"
        )

    def test_02_post_success_product(self):
        url = reverse(self.routes['url_list_products'])
        response = self.client.post(
            url,
            self.data_success_product_JSON(),
            format="json"
        )
        self.id = response.data['data']['id']

        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Method invalid"
        )