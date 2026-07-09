from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from unity.models import GameObjectTransform
from unity.serializers.game_object_transform_serializer import GameObjectTransformSerializer


class UpdateGameObjectTransformView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectTransformSerializer

    def put(self, request, game_object_transform_id=None):
        try:
            game_object_transform = GameObjectTransform.objects.get(pk=game_object_transform_id)
            serializer = GameObjectTransformSerializer(game_object_transform, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, game_object_transform_id=None):
        try:
            game_object_transform = GameObjectTransform.objects.get(pk=game_object_transform_id)
            serializer = GameObjectTransformSerializer(game_object_transform, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)