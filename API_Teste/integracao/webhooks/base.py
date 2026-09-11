# integracao/webhooks/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class ResultadoValidacao:
    valido: bool
    motivo: str = ''
    delivery_id: str = ''
    timestamp: Optional[int] = None


class WebhookAuthStrategy(ABC):
    """
    Contrato: receber request Django + credenciais decifradas + params,
    devolver ResultadoValidacao.
    """

    def __init__(self, sistema: Any, segredos: dict, params: dict):
        self.sistema = sistema
        self.segredos = segredos  # {'atual': 'xxx', 'anterior': 'yyy' ou None}
        self.params = params or {}

    @abstractmethod
    def validar(self, request) -> ResultadoValidacao:
        ...