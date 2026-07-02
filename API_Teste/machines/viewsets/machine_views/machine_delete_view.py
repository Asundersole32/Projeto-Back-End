from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from machines.models import Machine
from machines.serializers.machine_serializer import MachineSerializer


class DeleteMachineView(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = MachineSerializer

    def delete(self, request, machine_id=None):
        try:
            machine = Machine.objects.get(pk=machine_id)
            machine.delete()
            return Response({'message': 'Maquina deletada com sucesso.'}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)