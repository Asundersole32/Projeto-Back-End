from rest_framework import serializers

from unity.models import Metadata


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Metadata
        fields=['id', 'created_at', 'updated_at', 'scene', 'gameobject']
