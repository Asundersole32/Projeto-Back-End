from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import Prefab
from unity.serializers.prefab_serializer import PrefabSerializer


class GetPrefabView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrefabSerializer

    def get(self, request, prefab_id=None):
        try:
            prefab = Prefab.objects.get(pk=prefab_id)
            serializer = PrefabSerializer(prefab)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
