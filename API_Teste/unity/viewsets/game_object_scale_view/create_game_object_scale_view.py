from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from unity.serializers.game_object_scale_serializer import GameObjectScaleSerializer


class CreateGameObjectScaleView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameObjectScaleSerializer

    def post(self, request):
        try:
            serializer = GameObjectScaleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)