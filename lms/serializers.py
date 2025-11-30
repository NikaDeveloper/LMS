from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .validators import YouTubeValidator
from .models import Course, Lesson, Subscription


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            YouTubeValidator(field='video_url')
        ]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()

    is_subscribed = serializers.SerializerMethodField()

    lessons = LessonSerializer(many=True, read_only=True)

    def get_is_subscribed(self, obj):
        # Получаем текущего пользователя из контекста запроса
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Проверяем, есть ли запись в таблице Subscription
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, obj):
        return obj.lessons.count()
