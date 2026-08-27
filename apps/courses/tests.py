from django.test import TestCase
from apps.courses.models import Course
from apps.accounts.models import User # Import the User model
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from apps.infras.tests.base_tests import BaseViewTestClass


class CourseCreateTest(BaseViewTestClass):
    def setUp(self):
        self.url = reverse('create-course')
        self.user = self.regular_user
        print(self.user.id)
    def test_create_course_returns_201(self):
        start_date = timezone.make_aware(datetime(2025, 1, 1, 9, 0, 0))
        end_date = timezone.make_aware(datetime(2025, 1, 31, 17, 0, 0))

        payload = {
            "title": "Test Course",
            "teacher": self.user.id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        response = self.client.post(self.url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Course.objects.filter(title="Test Course").exists())
