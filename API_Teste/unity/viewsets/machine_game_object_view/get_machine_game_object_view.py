from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from unity.models import MachineGameObject
from unity.serializers.machine_game_object_serializer import MachineGameObjectSerializer


class GetMachineGameObjectView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MachineGameObjectSerializer

    def get(self, request, machine_game_object_id=None):
        try:
            machine_game_object = MachineGameObject.objects.get(pk=machine_game_object_id)
            serializer = MachineGameObjectSerializer(machine_game_object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
