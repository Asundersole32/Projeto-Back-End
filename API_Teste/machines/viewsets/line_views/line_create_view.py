from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from machines.serializers.line_serializer import LineSerializer


class CreateLineView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LineSerializer

    def post(self, request):
        try:
            serializer = LineSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)