from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from users.serializers.custom_user_register_serializer import CustomUserRegisterSerializer


class CreateUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserRegisterSerializer

    def post(self, request):
        try:
            serializer = CustomUserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)