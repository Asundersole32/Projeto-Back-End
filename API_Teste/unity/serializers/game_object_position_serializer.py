from rest_framework import serializers

from unity.models import GameObjectPosition


class GameObjectPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model=GameObjectPosition
        fields=['id', 'game_object_transform', 'x', 'y', 'z']
