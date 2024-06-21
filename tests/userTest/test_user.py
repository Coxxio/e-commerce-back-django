from src.apps.users.enums.UserRole import UserEnum
from ..test_setup import TestSetup

from django.urls import reverse

from rest_framework import status


class UsersAPITestCase(TestSetup):

    def data_success_client_JSON(self):
        return {
            "email": "client@ecommerce.com",
            "password": "25414411Aa",
            "person": {
                "fullName": "Antonio Cortez",
                "country": "Venecolandia",
                "phoneNumber": "04248403661",
                "codePostal": "6101"
            }
        }

    def data_success_admin_JSON(self):
        return {
            "email": "admin@ecommerce.com",
            "password": "25414411Aa",
            "person": {
                "fullName": "Antonio Cortez",
                "country": "Venecolandia",
                "phoneNumber": "04248403661",
                "codePostal": "6101"
            }
        }

    def data_success_update_JSON(self):
        return {
            "email": "ecommerce2@superadmin.com",
            "person": {
                "fullName": "Antonio updated Cortez",
                "country": "Venecolandia",
                "phoneNumber": "04248403661",
                "codePostal": "6101"
            }
        }

    def data_invalid_email_JSON(self):
        return {
            "email": "ADMINecommerce.com",
            "password": "25414411Aa",
            "person": {
                "fullName": "Antonio Cortez",
                "country": "Venecolandia",
                "phoneNumber": "04248403661",
                "codePostal": "6101"
            }
        }

    def data_repeat_email_JSON(self):
        return {
            "email": "ecommerce@client.com",
            "password": "25414411Aa",
            "person": {
                "fullName": "Antonio Cortez",
                "country": "Venecolandia",
                "phoneNumber": "04248403661",
                "codePostal": "6101"
            }
        }

    def data_password(self):
        return {
            "password": "25414411Aa",
        }

    def test_00_get_all_users(self):
        url = reverse(self.routes['url_user_list'])
        response = self.client.get(url, format="json")
        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Method invalid"
        )

    def test_01_get_one_user(self):
        url = reverse(self.routes['url_retrieve_destroy'], kwargs={
                      'pk': "85ffffb7-c173-41b9-9549-51637a9ca849"})
        response = self.client.get(url)

        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_02_post_success_client(self):
        url = reverse(self.routes['url_user_list'])
        response = self.client.post(
            url,
            self.data_success_client_JSON(),
            format="json"
        )
        self.id = response.data['data']['id']

        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Method invalid"
        )
        self.assertEqual(
            response.data['data']['role'],
            UserEnum.CLIENT
        )

    def test_03_post_success_admin(self):
        url = reverse(self.routes['url_admin_create'])
        response = self.client.post(
            url,
            self.data_success_admin_JSON(),
            format="json"
        )

        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Method invalid"
        )
        self.assertEqual(
            response.data['data']['role'],
            UserEnum.ADMIN
        )

    def test_04_post_fail(self):
        url = reverse(self.routes['url_user_list'])
        response = self.client.post(
            url,
            self.data_invalid_email_JSON(),
            format="json"
        )

        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data['errors']['email'][0],
            'Enter a valid email address.'
        )

    def test_05_post_email_repeat(self):
        url = reverse(self.routes['url_user_list'])
        response = self.client.post(
            url,
            self.data_repeat_email_JSON(),
            format="json"
        )

        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "El status code no coincide"
        )
        self.assertEqual(
            response.data['errors']['email'][0],
            f"user model with this Email already exists."
        )

    def test_06_update_user(self):
        url = reverse(self.routes['url_user_list'])
        response = self.client.patch(
            url,
            self.data_success_update_JSON(),
            format="json"
        )

        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_202_ACCEPTED,
            "Method invalid"
        )
        self.assertEqual(
            response.data['data']['email'],
            'ecommerce2@superadmin.com'
        )
        self.assertEqual(
            response.data['data']['person']['fullName'],
            'Antonio updated Cortez'
        )

    def test_07_update_repeat_email_user(self):
        url = reverse(self.routes['url_user_list'])
        response = self.client.patch(
            url,
            self.data_repeat_email_JSON(),
            format="json"
        )

        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
            "El status code no coincide"
        )
        self.assertEqual(
            response.data['msg'],
            'this email is already registered with another user'
        )

    def test_08_update_password(self):
        url = reverse(self.routes['url_update_pass'])
        response = self.client.patch(
            url,
            self.data_password(),
            format="json"
        )

        # Tests
        self.assertEqual(
            response.status_code,
            status.HTTP_202_ACCEPTED,
            "El status code no coincide"
        )
        self.assertEqual(
            response.data['msg'],
            'Password updated'
        )

    def test_09_delete_user(self):
        url = reverse(self.routes['url_retrieve_destroy'], kwargs={
                      'pk': "f4fc27db-14e5-493b-8460-8d8a29f37ae7"})
        response = self.client.delete(url)

        # Tests
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
