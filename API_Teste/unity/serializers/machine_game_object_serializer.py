from rest_framework import serializers

from unity.models import MachineGameObject


class MachineGameObjectSerializer(serializers.ModelSerializer):
    machine = serializers.StringRelatedField()

    class Meta:
        model=MachineGameObject
        fields=['id', 'game_object', 'machine']