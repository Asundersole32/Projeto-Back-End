from rest_framework import serializers

from unity.models import GameObjectScale


class GameObjectScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model=GameObjectScale
        fields=['id', 'game_object_transform', 'x', 'y', 'z']