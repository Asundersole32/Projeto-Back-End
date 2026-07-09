from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from machines.models import Machine
from machines.serializers.machine_serializer import MachineSerializer


class UpdateMachineView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MachineSerializer

    def put(self, request, machine_id=None):
        try:
            machine = Machine.objects.get(pk=machine_id)
            serializer = MachineSerializer(machine, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, machine_id=None):
        try:
            machine = Machine.objects.get(pk=machine_id)
            serializer = MachineSerializer(machine, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)