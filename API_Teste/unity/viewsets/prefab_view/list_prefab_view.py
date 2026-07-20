from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import Prefab
from unity.serializers.prefab_serializer import PrefabSerializer


class ListPrefabView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrefabSerializer

    def get(self, request):
        try:
            prefabs = Prefab.objects.all()
            serializer = PrefabSerializer(prefabs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
