from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import GameObject
from unity.serializers.game_object_serializer import GameObjectSerializer


class ListGameObjectView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectSerializer

    def get(self, request):
        try:
            game_object = GameObject.objects.all()
            serializer = GameObjectSerializer(game_object, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
