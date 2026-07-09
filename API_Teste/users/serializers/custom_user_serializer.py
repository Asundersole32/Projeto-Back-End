from rest_framework import serializers

from users.models import CustomUser


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=CustomUser
        fields=['email', 'first_name', 'last_name', 'username']
        read_only_fields=['email']