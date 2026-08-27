from django.urls import path
from .views import CourseCreateAPIView

urlpatterns = [
    path("courses/", CourseCreateAPIView.as_view(), name="create-course"),
]
