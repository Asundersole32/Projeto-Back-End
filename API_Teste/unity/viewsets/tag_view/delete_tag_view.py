from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from unity.models import Tag
from unity.serializers.tag_serializer import TagSerializer


class DeleteTagView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def delete(self, request, tag_id=None):
        try:
            tag = Tag.objects.get(pk=tag_id)
            tag.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)