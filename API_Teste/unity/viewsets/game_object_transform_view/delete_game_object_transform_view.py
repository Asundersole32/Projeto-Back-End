from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from unity.models import GameObjectTransform
from unity.serializers.game_object_transform_serializer import GameObjectTransformSerializer


class DeleteGameObjectTransformView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectTransformSerializer

    def delete(self, request, game_object_transform_id=None):
        try:
            game_object_transform = GameObjectTransform.objects.get(pk=game_object_transform_id)
            game_object_transform.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)