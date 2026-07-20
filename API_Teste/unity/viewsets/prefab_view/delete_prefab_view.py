from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from unity.models import Prefab
from unity.serializers.prefab_serializer import PrefabSerializer


class DeletePrefabView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrefabSerializer

    def delete(self, request, prefab_id=None):
        try:
            prefab = Prefab.objects.get(pk=prefab_id)
            prefab.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)