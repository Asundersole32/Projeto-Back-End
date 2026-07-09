from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import Layer
from unity.serializers.layer_serializer import LayerSerializer


class ListLayerView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LayerSerializer

    def get(self, request):
        try:
            layer = Layer.objects.all()
            serializer = LayerSerializer(layer, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
