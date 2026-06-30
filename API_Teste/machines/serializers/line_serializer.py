from rest_framework import serializers

from machines.models import Line


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = ['id', 'line_name', 'machine_qtd', 'created_at', 'updated_at']
