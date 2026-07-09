from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from unity.models import Layer
from unity.serializers.layer_serializer import LayerSerializer


class UpdateLayerView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LayerSerializer

    def put(self, request, layer_id=None):
        try:
            layer = Layer.objects.get(pk=layer_id)
            serializer = LayerSerializer(layer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, layer_id=None):
        try:
            layer = Layer.objects.get(pk=layer_id)
            serializer = LayerSerializer(layer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)