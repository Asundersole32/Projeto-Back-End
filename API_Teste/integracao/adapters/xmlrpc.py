# integracao/adapters/xmlrpc.py
import xmlrpc.client
from .base import Adapter, RespostaAdapter
from ..engine.registry import registrar_adapter


@registrar_adapter('XMLRPC')
class XmlRpcAdapter(Adapter):
    def executar(self, payload):
        url = self.sistema.base_url.rstrip('/') + '/' + self.operacao.caminho.lstrip('/')
        proxy = xmlrpc.client.ServerProxy(url, allow_none=True)
        metodo = self.operacao.adapter_params.get('operation_name') or self.operacao.codigo
        args = payload.get('args', [])
        kwargs = payload.get('kwargs', {})
        resultado = getattr(proxy, metodo)(*args, **kwargs)
        if not isinstance(resultado, dict):
            resultado = {'resultado': resultado}
        return RespostaAdapter(status_code=200, corpo=resultado, headers={})