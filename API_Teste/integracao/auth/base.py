# integracao/auth/base.py
from abc import ABC, abstractmethod


class AuthStrategy(ABC):
    """
    Contrato: recebe a instância de SistemaExterno (já com credenciais decifradas)
    e devolve um dict de headers/params a injetar na requisição.
    """

    def __init__(self, sistema, credenciais: dict, extra: dict):
        self.sistema = sistema
        self.credenciais = credenciais
        self.extra = extra

    @abstractmethod
    def aplicar(self, headers: dict, params: dict) -> tuple[dict, dict]:
        ...