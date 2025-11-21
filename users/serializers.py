from rest_framework import serializers
from .models import User, Payment


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Включаем только поля для просмотра и редактирования
        fields = ("id", "email", "first_name", "last_name", "phone", "city", "avatar")
        read_only_fields = ("email",)  # Запрещаем менять email через профиль


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
