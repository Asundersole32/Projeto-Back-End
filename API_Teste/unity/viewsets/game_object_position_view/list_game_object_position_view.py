from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import GameObjectPosition
from unity.serializers.game_object_position_serializer import GameObjectPositionSerializer


class ListGameObjectsPositionView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectPositionSerializer

    def get(self, request):
        try:
            game_object_position = GameObjectPosition.objects.all()
            serializer = GameObjectPositionSerializer(game_object_position, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
