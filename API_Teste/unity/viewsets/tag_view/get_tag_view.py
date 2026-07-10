from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import Tag
from unity.serializers.tag_serializer import TagSerializer


class GetTagView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def get(self, request, metadata_id=None):
        try:
            tag = Tag.objects.get(pk=metadata_id)
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
