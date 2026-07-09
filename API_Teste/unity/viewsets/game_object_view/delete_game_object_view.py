from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from unity.models import GameObject
from unity.serializers.game_object_serializer import GameObjectSerializer


class DeleteGameObjectView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectSerializer

    def delete(self, request, game_object_id=None):
        try:
            game_object = GameObject.objects.get(pk=game_object_id)
            game_object.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)