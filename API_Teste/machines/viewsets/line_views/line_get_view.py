from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from machines.serializers.line_serializer import LineSerializer
from machines.models import Line


class GetLineView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = LineSerializer

    def get(self, request, line_id=None):
        try:
            line = Line.objects.get(pk=line_id)
            serializer = LineSerializer(line)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)