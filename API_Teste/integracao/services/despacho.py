# integracao/services/despacho.py
from __future__ import annotations
from integracao.tasks import executar_integracao_async, _resolver_fila
from integracao.models import SistemaExterno, OperacaoIntegracao


def despachar_integracao(sistema_codigo: str, operacao_codigo: str, payload: dict,
                         correlation_id: str | None = None):
    """
    Enfileira uma integração na fila correta conforme prioridade configurada.
    Uso: em vez de chamar IntegrationEngine().executar() direto, chame isto.
    """
    sistema = SistemaExterno.objects.get(codigo=sistema_codigo)
    operacao = OperacaoIntegracao.objects.get(sistema=sistema, codigo=operacao_codigo)
    fila = _resolver_fila(sistema, operacao)
    return executar_integracao_async.apply_async(
        args=[sistema_codigo, operacao_codigo, payload, correlation_id],
        queue=fila,
    )