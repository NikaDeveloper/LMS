from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CourseViewSet,
    LessonViewSet,
)


app_name = "lms"


router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"lessons", LessonViewSet, basename="lesson")


urlpatterns = [

]

urlpatterns += router.urls
