from rest_framework import serializers

from ..models.user_model import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=CustomUser
        fields=["username", "first_name", "last_name", "email", "is_active"]