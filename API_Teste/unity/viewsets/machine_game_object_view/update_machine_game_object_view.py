from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from unity.models import MachineGameObject
from unity.serializers.machine_game_object_serializer import MachineGameObjectSerializer


class UpdateMachineGameObjectView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MachineGameObjectSerializer

    def put(self, request, machine_game_object_id=None):
        try:
            machine_game_object = MachineGameObject.objects.get(pk=machine_game_object_id)
            serializer = MachineGameObjectSerializer(machine_game_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, machine_game_object_id=None):
        try:
            machine_game_object = MachineGameObject.objects.get(pk=machine_game_object_id)
            serializer = MachineGameObjectSerializer(machine_game_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)