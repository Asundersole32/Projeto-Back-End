# integracao/engine/exceptions.py
class IntegracaoError(Exception):
    """Base para todos os erros de integração."""


class OperacaoNaoEncontrada(IntegracaoError):
    """Configuração inexistente ou inativa."""


class SistemaBloqueado(IntegracaoError):
    """Circuit breaker aberto."""


class MapeamentoError(IntegracaoError):
    """Erro determinístico no mapeamento — NÃO faz retry."""


class ErroTransiente(IntegracaoError):
    """Falha temporária (timeout, 5xx, connection) — FAZ retry."""

    def __init__(self, mensagem, retry_after=None):
        super().__init__(mensagem)
        self.retry_after = retry_after


class ErroDefinitivo(IntegracaoError):
    """Falha determinística (400, 401, 403, 422, regra de negócio) — NÃO faz retry."""


class ErroRateLimit(ErroTransiente):
    """HTTP 429 — retry com backoff longo."""


def classificar_erro(excecao: Exception) -> str:
    """
    Retorna 'transiente', 'definitivo' ou 'rate_limit'.
    Usado pela task Celery para decidir se retenta.
    """
    import requests
    from requests.exceptions import Timeout, ConnectionError as RequestsConnectionError

    if isinstance(excecao, ErroRateLimit):
        return 'rate_limit'
    if isinstance(excecao, ErroTransiente):
        return 'transiente'
    if isinstance(excecao, (ErroDefinitivo, MapeamentoError, SistemaBloqueado, OperacaoNaoEncontrada)):
        return 'definitivo'

    # Timeouts / conexão → transiente
    if isinstance(excecao, (Timeout, RequestsConnectionError)):
        return 'transiente'

    # HTTPError: olhar o status code
    if isinstance(excecao, requests.exceptions.HTTPError):
        code = getattr(excecao.response, 'status_code', 0)
        if code == 429:
            return 'rate_limit'
        if code in (500, 502, 503, 504):
            return 'transiente'
        if 400 <= code < 500:
            return 'definitivo'
        return 'transiente'

    # Exceções nativas de rede
    if isinstance(excecao, (ConnectionError, OSError, TimeoutError)):
        return 'transiente'

    # Por padrão, conservador: definitivo (não retenta o que não conhecemos)
    return 'definitivo'