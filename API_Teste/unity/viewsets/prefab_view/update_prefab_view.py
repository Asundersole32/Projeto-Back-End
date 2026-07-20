from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from unity.models import Prefab
from unity.serializers.prefab_serializer import PrefabSerializer


class UpdatePrefabView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrefabSerializer

    def put(self, request, prefab_id=None):
        try:
            prefab = Prefab.objects.get(pk=prefab_id)
            serializer = PrefabSerializer(prefab, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, prefab_id=None):
        try:
            prefab = Prefab.objects.get(pk=prefab_id)
            serializer = PrefabSerializer(prefab, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)