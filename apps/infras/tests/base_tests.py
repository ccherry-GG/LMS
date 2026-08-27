from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from apps.accounts.models import User
from django.test.testcases import TestCase
from apps.infras.constants.accounts.urls_constants import ACCOUNT_USERS_LIST, ACCOUNTS_USERS_DETAIL
from custom_logger import custom_logger


class BaseViewTestClass(APITestCase):
    """
    BaseViewTestClass provides a foundation for API view tests.
    It sets up test data with admin, staff, and regular users.
    The class offers authentication helpers, URL utilities, and request wrappers.
    Assertion methods for common HTTP status checks are included.
    Convenience methods for CRUD operations on the user endpoint are provided.

    Some helper methods:
    - authenticate_as_admin(): Authenticate the test client as the admin user.
    - logout(): Log out the test client.
    - refresh(instance): Refresh a model instance from the database.
    """

    @classmethod
    def setUpTestData(cls):
        cls.password = "TestPass123!"
        cls.admin_user = cls._create_user(
            username='adminuser',
            password='SoMerand0mP@ssfoRadmin',
            email="admin@example.com",
            phone_number = '09933004562',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        cls.staff_user = cls._create_user(
            username='staffuser',
            password='SoMerand0mP@ssfoRstaff',
            email="staff@example.com",
            phone_number = '09933004565',
            is_staff=True,
            is_active=True,
        )
        cls.regular_user = cls._create_user(
            username='regularuser',
            password='SoMerand0mP@ssfoRregular',
            email="user@example.com",
            phone_number = '09933004566',
            is_active=True,
        )

    @classmethod
    def _create_user(cls, email, is_superuser=False, is_staff=False, is_active=True, **extra):
        """
        Creates a User with the given email and flags,
        sets password if missing, saves, and returns the user.
        """
        user = User(email=email, is_superuser=is_superuser, is_staff=is_staff, is_active=is_active, **extra)
        try:
            if not user.password:
                user.set_password(cls.password)
        except Exception:
            pass
        user.save()
        return user

    def setUp(self):
        self.client = APIClient()
        self.users_url = reverse(ACCOUNT_USERS_LIST)
        self.users = User.objects.all()
        print(self.users)

    # Authentication helpers
    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def authenticate_as_admin(self):
        self.authenticate(self.admin_user)

    def authenticate_as_staff(self):
        self.authenticate(self.staff_user)

    def authenticate_as_regular(self):
        self.authenticate(self.regular_user)

    def logout(self):
        self.client.force_authenticate(user=None)

    # URL helpers
    def user_detail_url(self, pk):
        return reverse(ACCOUNTS_USERS_DETAIL, args=[pk])

    # Request helpers
    def get(self, url, params=None, **kwargs):
        return self.client.get(url, params or {}, format='json', **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.client.post(url, data or {}, format='json', **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.client.put(url, data or {}, format='json', **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.client.patch(url, data or {}, format='json', **kwargs)

    def delete(self, url, **kwargs):
        return self.client.delete(url, format='json', **kwargs)

    # Users endpoint convenience methods
    def list_users(self, params=None):
        return self.get(self.users_url, params=params)

    def create_user(self, data=None):
        return self.post(self.users_url, data=data)

    def retrieve_user(self, pk):
        return self.get(self.user_detail_url(pk))

    def update_user(self, pk, data=None):
        return self.put(self.user_detail_url(pk), data=data)

    def partial_update_user(self, pk, data=None):
        return self.patch(self.user_detail_url(pk), data=data)

    def delete_user(self, pk):
        return self.delete(self.user_detail_url(pk))

    # Assertion helpers
    def assertStatusCode(self, response, expected_status):
        self.assertEqual(response.status_code, expected_status)

    def assertOK(self, response):
        self.assertStatusCode(response, status.HTTP_200_OK)

    def assertCreated(self, response):
        self.assertStatusCode(response, status.HTTP_201_CREATED)

    def assertNoContent(self, response):
        self.assertStatusCode(response, status.HTTP_204_NO_CONTENT)

    def assertBadRequest(self, response):
        self.assertStatusCode(response, status.HTTP_400_BAD_REQUEST)

    def assertUnauthorized(self, response):
        self.assertStatusCode(response, status.HTTP_401_UNAUTHORIZED)

    def assertForbidden(self, response):
        self.assertStatusCode(response, status.HTTP_403_FORBIDDEN)

    def assertNotFound(self, response):
        self.assertStatusCode(response, status.HTTP_404_NOT_FOUND)

    def assertListResponse(self, response):
        self.assertOK(response)
        data = response.data
        self.assertTrue(isinstance(data, (list, dict)))
        if isinstance(data, dict):
            self.assertIn('results', data)

    # Utilities
    def refresh(self, instance):
        """
        Refresh the given Django model instance from the database.
        Use in tests to get the latest state after mutations or side effects.
        Param: instance (Model) - object to re-fetch by primary key.
        Return: freshly loaded instance of the same model.
        Raises: DoesNotExist if the instance no longer exists.
        """
        return instance.__class__.objects.get(pk=instance.pk)
