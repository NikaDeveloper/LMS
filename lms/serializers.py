from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .validators import YouTubeValidator
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            YouTubeValidator(field='video_url')
        ]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()

    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, obj):
        return obj.lessons.count()
