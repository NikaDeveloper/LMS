from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
