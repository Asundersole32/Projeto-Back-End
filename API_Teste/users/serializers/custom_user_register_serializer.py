from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.models import CustomUser


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'username', 'is_admin', 'is_active', 'is_staff', 'is_superuser',  'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user