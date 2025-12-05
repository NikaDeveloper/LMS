from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonViewSet, SubscriptionAPIView


app_name = "lms"


router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"lessons", LessonViewSet, basename="lesson")


urlpatterns = [
    path("courses/subscribe/", SubscriptionAPIView.as_view(), name="course_subscribe"),
]

urlpatterns += router.urls
