from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status

from machines.models import Line
from machines.serializers.line_serializer import LineSerializer


class UpdateLineView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LineSerializer

    def put(self, request, line_id=None):
        try:
            line = Line.objects.get(pk=line_id)
            serializer = LineSerializer(line, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, line_id=None):
        try:
            Line = Line.objects.get(pk=line_id)
            serializer = LineSerializer(Line, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)