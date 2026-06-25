from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from drf_yasg import openapi
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema


class CustomObtainAuthToken(ObtainAuthToken):
    @swagger_auto_schema(
        operation_description="Endpoint de login com email e senha",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            },
        ),
        responses={200: 'sucesso'},
    )


    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"error": "Credenciais inválidas. Verifique seu e-mail e senha."}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "username": user.username,
                "uid": user.uid,
                "email": user.email,
            }
        })
    