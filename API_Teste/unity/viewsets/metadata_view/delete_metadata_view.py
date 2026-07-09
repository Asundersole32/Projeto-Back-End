from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from unity.models import Metadata
from unity.serializers.metadata_serializer import MetadataSerializer


class DeleteMetadataView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MetadataSerializer

    def delete(self, request, metadata_id=None):
        try:
            metadata = Metadata.objects.get(pk=metadata_id)
            metadata.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)