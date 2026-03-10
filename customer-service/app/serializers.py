from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer dùng để trả dữ liệu customer ra ngoài (không bao gồm password)."""

    class Meta:
        model = Customer
        fields = ["id", "name", "email"]


class CustomerRegisterSerializer(serializers.ModelSerializer):
    """Serializer dùng cho đăng ký, có password (write-only)."""

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Customer
        fields = ["id", "name", "email", "password"]

    def create(self, validated_data):
        from django.contrib.auth.hashers import make_password

        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)