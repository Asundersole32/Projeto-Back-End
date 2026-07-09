from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import GameObjectTransform
from unity.serializers.game_object_transform_serializer import GameObjectTransformSerializer


class ListGameObjectTransformView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectTransformSerializer

    def get(self, request):
        try:
            game_object_transform = GameObjectTransform.objects.all()
            serializer = GameObjectTransformSerializer(game_object_transform, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
