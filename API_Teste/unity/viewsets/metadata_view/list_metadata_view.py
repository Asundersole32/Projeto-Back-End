from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import Metadata
from unity.serializers.metadata_serializer import MetadataSerializer


class ListMetadataView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MetadataSerializer

    def get(self, request):
        try:
            metadata = Metadata.objects.all()
            serializer = MetadataSerializer(metadata, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
