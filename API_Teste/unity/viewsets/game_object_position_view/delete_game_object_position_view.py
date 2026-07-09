from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from unity.models import GameObjectPosition
from unity.serializers.game_object_position_serializer import GameObjectPositionSerializer


class DeleteGameObjectPositionView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectPositionSerializer

    def delete(self, request, game_object_position_id=None):
        try:
            game_object_position = GameObjectPosition.objects.get(pk=game_object_position_id)
            game_object_position.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)