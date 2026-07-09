from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from unity.models import GameObject
from unity.serializers.game_object_serializer import GameObjectSerializer


class UpdateGameObjectView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectSerializer

    def put(self, request, game_object_id=None):
        try:
            game_object = GameObject.objects.get(pk=game_object_id)
            serializer = GameObjectSerializer(game_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, game_object_id=None):
        try:
            game_object = GameObject.objects.get(pk=game_object_id)
            serializer = GameObjectSerializer(game_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)