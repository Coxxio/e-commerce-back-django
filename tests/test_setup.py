from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class TestSetup(APITestCase):
    fixtures = ['tests/fixtures/UserAdmin.json']
    
    def setUp(self):
        # URLS User Module
        self.login_url = 'login'
        self.url_user_list = 'user_list_create_update'
        self.url_admin_create = 'user_admin_create'
        self.url_retrieve_destroy = 'user_retrieve_destroy'
        self.url_update_pass = 'user_update_password'
        self.url_destroy_self = 'user_delete_self'

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


        url = reverse(self.login_url)
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
        self.login_url = "login"
        self.url_destroy_self = 'user_delete_self'
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
        
        url = reverse(self.login_url)
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
