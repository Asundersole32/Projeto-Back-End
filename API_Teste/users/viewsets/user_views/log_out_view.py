from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Logout realizado com sucesso."}, status=200)
        except Token.DoesNotExist:
            return Response({"error": "Usuário não estava logado."}, status=400)