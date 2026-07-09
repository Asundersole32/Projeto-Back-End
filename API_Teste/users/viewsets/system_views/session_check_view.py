from rest_framework import status, authentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class SessionCheckView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'authenticated': True,
            'first_name': user.first_name,
            'uid': user.uid,
            'email': user.email,
            'user_type': user.user_type,
        }, status=status.HTTP_200_OK)