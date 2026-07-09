from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from unity.models import GameObjectPosition
from unity.serializers.game_object_position_serializer import GameObjectPositionSerializer


class UpdateGameObjectRotationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectPositionSerializer

    def put(self, request, game_object_rotation_id=None):
        try:
            game_object_rotation = GameObjectPosition.objects.get(pk=game_object_rotation_id)
            serializer = GameObjectPositionSerializer(game_object_rotation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, game_object_rotation_id=None):
        try:
            game_object_rotation = GameObjectPosition.objects.get(pk=game_object_rotation_id)
            serializer = GameObjectPositionSerializer(game_object_rotation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)