from rest_framework import generics, status
from rest_framework.permissions import AllowAny


class GetMachineView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PetSerializer

    def get(self, request, pet_id=None):
        try:
            pet = Pet.objects.get(pk=pet_id)
            serializer = PetSerializer(pet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)