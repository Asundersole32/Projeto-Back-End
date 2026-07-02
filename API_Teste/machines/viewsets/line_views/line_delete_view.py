from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from machines.models import Line
from machines.serializers.line_serializer import LineSerializer


class DeleteLineView(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = LineSerializer

    def delete(self, request, line_id=None):
        try:
            line = Line.objects.get(pk=line_id)
            line.delete()
            return Response({'message': 'Linha deletada com sucesso.'}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)