# integracao/adapters/rest.py
import requests
from .base import Adapter, RespostaAdapter
from ..engine.registry import registrar_adapter


@registrar_adapter('REST')
class RestAdapter(Adapter):
    def executar(self, payload):
        url = self.sistema.base_url.rstrip('/') + '/' + self.operacao.caminho.lstrip('/')
        headers = {**self.sistema.headers_padrao, **self.headers}
        if self.operacao.content_type:
            headers.setdefault('Content-Type', self.operacao.content_type)
        headers.setdefault('Accept', 'application/json')

        resp = requests.request(
            method=self.operacao.metodo_http,
            url=url,
            headers=headers,
            params=self.params or None,
            json=payload if payload else None,
            timeout=self.timeout,
            verify=self.verify_ssl,
        )
        try:
            corpo = resp.json() if resp.content else {}
        except ValueError:
            corpo = {'_raw': resp.text}

        return RespostaAdapter(status_code=resp.status_code, corpo=corpo, headers=dict(resp.headers))