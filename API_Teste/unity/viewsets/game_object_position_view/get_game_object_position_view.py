from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import GameObjectPosition
from unity.serializers.game_object_position_serializer import GameObjectPositionSerializer


class GetGameObjectPositionView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectPositionSerializer

    def get(self, request, game_object_position_id=None):
        try:
            game_object_position = GameObjectPosition.objects.get(pk=game_object_position_id)
            serializer = GameObjectPositionSerializer(game_object_position)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
