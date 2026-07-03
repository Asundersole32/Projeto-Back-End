from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from machines.models import MachineData, Machine
from machines.serializers.machine_data_serializer import MachineDataSerializer


class GetSeededMachineDataView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MachineDataSerializer

    def get(self, request, machine_id=None):
        try:
            machine = Machine.objects.get(pk=machine_id)
            machine_data = MachineData.objects.filter(machine=machine).last()
            serializer = MachineDataSerializer(machine_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)