from rest_framework import serializers

from unity.models import Layer


class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Layer
        fields=['id', 'layer_name']
