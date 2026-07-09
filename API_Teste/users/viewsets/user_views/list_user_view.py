from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.repository.user_repository import UserFilter
from users.serializers.custom_user_serializer import CustomUserDetailsSerializer
from users.models import CustomUser


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserDetailsSerializer
    queryset = CustomUser.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as error:
            return Response({'message': str(error)},status=status.HTTP_400_BAD_REQUEST)
