from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from unity.models import Metadata
from unity.serializers.metadata_serializer import MetadataSerializer


class UpdateMetadataView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MetadataSerializer

    def put(self, request, metadata_id=None):
        try:
            metadata = Metadata.objects.get(pk=metadata_id)
            serializer = MetadataSerializer(metadata, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, metadata_id=None):
        try:
            metadata = Metadata.objects.get(pk=metadata_id)
            serializer = MetadataSerializer(metadata, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)