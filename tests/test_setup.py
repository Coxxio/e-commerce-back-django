from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .routes.routes import routes

class TestSetup(APITestCase):
    fixtures = ['tests/fixtures/UserAdmin.json']
    
    def setUp(self):
        # URLS User Module
        self.routes = routes
        self.category_id_test = 'f4fc27db-14e5-493b-8460-8d8a29f37ae7'
        self.category_id_test_2 = 'de0e6f32-bc71-4402-a595-516e7bd4db0c'

        # Data
        self.data_super_admin = {
            "email": "ecommerce@superadmin.com",
            "password": "12345678Super",
            "role": "SUPER_ADMIN",
            "person": {
                "fullName": "Antonio Cortez",
                "country": "Venecolandia",
                "phoneNumber": "04248403661",
                "codePostal": "6101"
            }
        }
        self.data_admin = {
            "email": "ecommerce@admin.com",
            "password": "12345678Admin",
            "role": "ADMIN",
            "person": {
                "fullName": "Antonio Cortez",
                "country": "Venecolandia",
                "phoneNumber": "04248403661",
                "codePostal": "6101"
            }
        }
        self.data_client = {
            "email": "ecommerce@client.com",
            "password": "12345678Client",
            "role": "ADMIN",
            "person": {
                "fullName": "Antonio Cortez",
                "country": "Venecolandia",
                "phoneNumber": "04248403661",
                "codePostal": "6101"
            }
        }


        url = reverse(self.routes['login_url'])
        response = self.client.post(
            url,
            {
                "email": self.data_super_admin['email'],
                "password": self.data_super_admin['password']
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.token = response.data['data']['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        return super().setUp()


class TestSetupClient(TestSetup):
    def setUp(self):
        self.routes = routes
        self.data_client = {
            "email": "ecommerce@client.com",
            "password": "12345678Admin",
            "role": "ADMIN",
            "person": {
                "fullName": "Antonio Cortez",
                "country": "Venecolandia",
                "phoneNumber": "04248403661",
                "codePostal": "6101"
            }
        }
        
        url = reverse(self.routes['login_url'])
        response = self.client.post(
            url,
            {
                "email": self.data_client['email'],
                "password": self.data_client['password']
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.token = response.data['data']['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        return super().setUp()
