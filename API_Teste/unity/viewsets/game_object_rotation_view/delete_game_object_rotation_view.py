from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from unity.models import GameObjectRotation
from unity.serializers.game_object_rotation_serializer import GameObjectRotationSerializer


class DeleteGameObjectRotationView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectRotationSerializer

    def delete(self, request, game_object_rotation_id=None):
        try:
            game_object_rotation = GameObjectRotation.objects.get(pk=game_object_rotation_id)
            game_object_rotation.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)