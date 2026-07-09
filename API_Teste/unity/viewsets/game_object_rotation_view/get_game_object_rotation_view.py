from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import GameObjectRotation
from unity.serializers.game_object_rotation_serializer import GameObjectRotationSerializer


class GetGameObjectRotationView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectRotationSerializer

    def get(self, request, game_object_rotation_id=None):
        try:
            game_object_rotation = GameObjectRotation.objects.get(pk=game_object_rotation_id)
            serializer = GameObjectRotationSerializer(game_object_rotation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
