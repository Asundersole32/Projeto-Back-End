from rest_framework import serializers

from unity.models import GameObject


class GameObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=GameObject
        fields=['id', 'name', 'tag', 'layer', 'prefab_name', 'parent']
