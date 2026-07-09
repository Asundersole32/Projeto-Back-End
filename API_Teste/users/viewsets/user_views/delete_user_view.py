from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from users.serializers.custom_user_serializer import CustomUserDetailsSerializer
from users.models import CustomUser


class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserDetailsSerializer

    def delete(self, request, uid=None):
        try:
            user = CustomUser.objects.get(uid=uid)
            user.delete()
            return Response({'message': 'Usuário deletado com sucesso.'}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)