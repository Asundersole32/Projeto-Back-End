from rest_framework import serializers

from unity.models import Prefab


class PrefabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prefab
        fields = ['id', 'prefab_name']
