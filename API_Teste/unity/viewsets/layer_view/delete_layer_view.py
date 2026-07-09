from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from unity.models import Layer
from unity.serializers.layer_serializer import LayerSerializer


class DeleteLayerView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LayerSerializer

    def delete(self, request, layer_id=None):
        try:
            layer = Layer.objects.get(pk=layer_id)
            layer.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)