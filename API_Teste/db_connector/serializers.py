from rest_framework import serializers

class ConnectionSerializer(serializers.Serializer):
    db_type = serializers.ChoiceField(choices=['postgresql', 'mysql', 'sqlite', 'oracle'])
    host = serializers.CharField(required=False, allow_blank=True)
    port = serializers.IntegerField(required=False, allow_null=True)
    user = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True, write_only=True)
    database = serializers.CharField()

    def validate(self, data):
        db_type = data.get('db_type')
        if db_type != 'sqlite':
            if not data.get('host'):
                raise serializers.ValidationError("host is required for this database type")
            if not data.get('port'):
                raise serializers.ValidationError("port is required for this database type")
            if not data.get('user'):
                raise serializers.ValidationError("user is required for this database type")
            # password pode ser vazia, mas permitimos
        return data