from rest_framework import serializers

from unity.models import GameObject


class GameObjectSerializer(serializers.ModelSerializer):
    prefab = serializers.StringRelatedField()

    class Meta:
        model=GameObject
        fields=['id', 'name', 'tag', 'layer', 'prefab', 'pre_existing_parent', 'line_position', 'parent']
