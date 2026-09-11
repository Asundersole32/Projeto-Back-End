# integracao/adapters/soap.py
import requests
from zeep import Client, Settings as ZeepSettings
from .base import Adapter, RespostaAdapter
from ..engine.registry import registrar_adapter


@registrar_adapter('SOAP')
class SoapAdapter(Adapter):
    def executar(self, payload):
        wsdl = self.operacao.adapter_params.get('wsdl_url')
        op_name = self.operacao.adapter_params.get('operation_name') or self.operacao.codigo

        client = Client(
            wsdl=wsdl,
            settings=ZeepSettings(extra_http_headers=self.headers),
            transport=self._transport(),
        )
        resultado = getattr(client.service, op_name)(**payload)
        # zeep devolve objetos; serializamos como dict
        from zeep.helpers import serialize_object
        corpo = serialize_object(resultado)
        if not isinstance(corpo, dict):
            corpo = {'resultado': corpo}
        return RespostaAdapter(status_code=200, corpo=corpo, headers={})

    def _transport(self):
        from zeep.transports import Transport
        session = requests.Session()
        session.verify = self.verify_ssl
        return Transport(session=session, timeout=self.timeout)