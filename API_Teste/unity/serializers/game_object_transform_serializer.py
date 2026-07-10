from rest_framework import serializers

from unity.models import GameObjectTransform


class GameObjectTransformSerializer(serializers.ModelSerializer):
    class Meta:
        model=GameObjectTransform
        fields=['id', 'game_object']
