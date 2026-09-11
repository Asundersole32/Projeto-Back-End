# integracao/adapters/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RespostaAdapter:
    status_code: int
    corpo: dict          # já normalizado para dict
    headers: dict


class Adapter(ABC):
    """Contrato universal de transporte."""

    def __init__(self, sistema, operacao, headers: dict, params: dict, timeout: int, verify_ssl: bool):
        self.sistema = sistema
        self.operacao = operacao
        self.headers = headers
        self.params = params
        self.timeout = timeout
        self.verify_ssl = verify_ssl

    @abstractmethod
    def executar(self, payload: dict) -> RespostaAdapter:
        ...