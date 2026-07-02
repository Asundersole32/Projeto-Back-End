from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from users.serializers.custom_user_serializer import CustomUserDetailsSerializer
from users.models import CustomUser


class GetUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserDetailsSerializer

    def get(self, request, uid=None):
        try:
            user = CustomUser.objects.get(uid=uid)
            serializer = CustomUserDetailsSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)