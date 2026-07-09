from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import GameObject
from unity.serializers.game_object_serializer import GameObjectSerializer


class GetGameObjectView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectSerializer

    def get(self, request, game_object_id=None):
        try:
            game_object = GameObject.objects.get(pk=game_object_id)
            serializer = GameObjectSerializer(game_object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
