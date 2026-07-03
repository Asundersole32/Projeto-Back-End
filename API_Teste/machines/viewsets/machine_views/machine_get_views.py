from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from machines.serializers.machine_serializer import MachineSerializer
from machines.models import Machine


class GetMachineView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MachineSerializer

    def get(self, request, machine_id=None):
        try:
            machine = Machine.objects.get(pk=machine_id)
            serializer = MachineSerializer(machine)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)