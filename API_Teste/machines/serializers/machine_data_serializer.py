from rest_framework import serializers

from machines.models import MachineData


class MachineDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineData
        fields = ['id', 'machine', 'data', 'created_at']
        depth = 1 
