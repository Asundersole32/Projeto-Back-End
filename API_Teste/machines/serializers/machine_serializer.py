from rest_framework import serializers

from machines.models import Machine


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'machine_name', 'machine_type', 'company', 'line', 'status', 'is_active', 'created_at', 'updated_at']
