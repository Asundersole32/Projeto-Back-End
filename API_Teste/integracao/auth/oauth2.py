# integracao/auth/oauth2.py
import time
import requests
from .base import AuthStrategy
from ..engine.registry import registrar_auth

# cache de tokens por sistema
_TOKEN_CACHE = {}  # {sistema_id: (expira_em, token)}


@registrar_auth('OAUTH2_CC')
class OAuth2ClientCredentials(AuthStrategy):
    def aplicar(self, headers, params):
        sid = self.sistema.id
        now = time.time()
        cached = _TOKEN_CACHE.get(sid)
        if cached and cached[0] > now + 30:
            headers['Authorization'] = f'Bearer {cached[1]}'
            return headers, params

        token_url = self.extra.get('token_url')
        resp = requests.post(token_url, data={
            'grant_type': 'client_credentials',
            'client_id': self.credenciais['client_id'],
            'client_secret': self.credenciais['client_secret'],
            'scope': self.extra.get('scope', ''),
        }, timeout=15)
        resp.raise_for_status()
        body = resp.json()
        token = body['access_token']
        expira = now + int(body.get('expires_in', 3600))
        _TOKEN_CACHE[sid] = (expira, token)
        headers['Authorization'] = f'Bearer {token}'
        return headers, params