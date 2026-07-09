from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from unity.models import GameObjectScale
from unity.serializers.game_object_scale_serializer import GameObjectScaleSerializer


class DeleteGameObjectScaleView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectScaleSerializer

    def delete(self, request, game_object_scale_id=None):
        try:
            game_object_scale = GameObjectScale.objects.get(pk=game_object_scale_id)
            game_object_scale.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)