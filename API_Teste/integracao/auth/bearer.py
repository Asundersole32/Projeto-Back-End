# integracao/auth/bearer.py
from .base import AuthStrategy
from ..engine.registry import registrar_auth


@registrar_auth('BEARER')
class BearerAuth(AuthStrategy):
    def aplicar(self, headers, params):
        token = self.credenciais.get('token', '')
        headers['Authorization'] = f'Bearer {token}'
        return headers, params