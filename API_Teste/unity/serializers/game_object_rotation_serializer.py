from rest_framework import serializers

from unity.models import GameObjectRotation


class GameObjectRotationSerializer(serializers.ModelSerializer):
    class Meta:
        model=GameObjectRotation
        fields=['id', 'game_object_transform', 'x', 'y', 'z']
