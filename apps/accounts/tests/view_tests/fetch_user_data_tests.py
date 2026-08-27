from rest_framework import status
from apps.accounts.models import User
from apps.infras.tests.base_tests import BaseViewTestClass
from custom_logger import custom_logger




class FetchUserInfos(BaseViewTestClass):
    def setUp(self):
        super().setUp()

    def test_fetch_users_data(self):
        custom_logger.info(f"Users: {self.users}")
        print("hello\n\n\nworld")
        response = self.client.get(self.users_url)
        custom_logger.info(f"Response: {response}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
