# integracao/auth/basic.py
import base64
from .base import AuthStrategy
from ..engine.registry import registrar_auth


@registrar_auth('BASIC')
class BasicAuth(AuthStrategy):
    def aplicar(self, headers, params):
        user = self.credenciais.get('usuario', '')
        pwd = self.credenciais.get('senha', '')
        raw = f'{user}:{pwd}'.encode()
        headers['Authorization'] = 'Basic ' + base64.b64encode(raw).decode()
        return headers, params