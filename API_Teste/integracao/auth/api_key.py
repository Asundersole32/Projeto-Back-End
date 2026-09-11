# integracao/auth/api_key.py
from .base import AuthStrategy
from ..engine.registry import registrar_auth


@registrar_auth('API_KEY')
class ApiKeyAuth(AuthStrategy):
    def aplicar(self, headers, params):
        chave = self.credenciais.get('chave', '')
        header_name = self.extra.get('header_name', 'X-API-Key')
        via_query = self.extra.get('via_query', False)
        if via_query:
            params[self.extra.get('query_name', 'api_key')] = chave
        else:
            headers[header_name] = chave
        return headers, params