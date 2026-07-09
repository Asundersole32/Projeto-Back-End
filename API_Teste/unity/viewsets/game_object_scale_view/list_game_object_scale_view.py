from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import GameObjectScale
from unity.serializers.game_object_scale_serializer import GameObjectScaleSerializer


class ListGameObjectScaleView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectScaleSerializer

    def get(self, request):
        try:
            game_object_scale = GameObjectScale.objects.all()
            serializer = GameObjectScaleSerializer(game_object_scale, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
