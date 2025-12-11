from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=CurrentUserDefault(),
    )

    class Meta:
        model = Payment
        fields = (
            "id",
            "user",
            "course",
            "lesson",
            "amount",
            "payment_method",
            "session_id",
            "link",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "city",
            "avatar",
            "payments",
        )
        read_only_fields = ("email",)  # Запрещаем менять email через профиль


class UserPublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "phone", "city", "avatar")


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "phone", "city", "avatar")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data.get("phone"),
            city=validated_data.get("city"),
            avatar=validated_data.get("avatar"),
        )
        return user
