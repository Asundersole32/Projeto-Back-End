# integracao/engine/engine.py
from __future__ import annotations

"""
Motor de integração universal.

Contém APENAS a classe IntegrationEngine. Nada de registro de adapters/auth/
transforms aqui — isso vive em `registry.py`.
"""

import time
import uuid
import logging
from copy import deepcopy
from datetime import timedelta

from django.utils import timezone

from .registry import obter_adapter, obter_auth
from .mapper import mapear, _get_path
from .crypto import decifrar
from .exceptions import (
    SistemaBloqueado,
    OperacaoNaoEncontrada,
    ErroRateLimit,
    ErroTransiente,
    ErroDefinitivo,
)
from ..models import (
    SistemaExterno,
    OperacaoIntegracao,
    MapeamentoCampo,
    RegistroIntegracao,
    Direcao,
)

logger = logging.getLogger(__name__)

LIMITE_FALHAS = 5
TEMPO_BLOQUEIO_MINUTOS = 5


def _mascarar_segredos(headers: dict) -> dict:
    """Substitui valores sensíveis por máscara para exibir em dry-run/logs."""
    SENSIVEIS = {'authorization', 'x-api-key', 'apikey', 'x-auth-token', 'cookie'}
    return {
        k: ('***' if k.lower() in SENSIVEIS else v)
        for k, v in headers.items()
    }


class IntegrationEngine:
    """
    Executa qualquer operação de integração a partir de configuração em banco.
    Não conhece nenhum ERP/MES específico.
    """

    # ========================================================================
    # DRY-RUN — resolve tudo EXCETO a chamada HTTP
    # ========================================================================

    def dry_run(
        self,
        sistema_codigo: str,
        operacao_codigo: str,
        payload: dict,
        payload_resposta_simulado: dict | None = None,
        rodar_auth: bool = False,
    ) -> dict:
        """
        Simula a execução completa do pipeline sem chamar o sistema externo.

        Args:
            payload: payload canônico de entrada
            payload_resposta_simulado: opcional. Se passado, roda também o mapper
                de RESPONSE sobre ele e mostra o canônico resultante.
            rodar_auth: se True, executa a strategy de auth (útil para validar
                OAuth2 sem chamar o endpoint de negócio). Se False, pula e
                mascara headers como '***'.

        Returns:
            dict com:
              - payload_entrada
              - payload_mapeado (o que SERIA enviado)
              - request_preview: { method, url, headers, params, content_type }
              - response_preview: (se payload_resposta_simulado)
              - validacoes: lista de avisos/erros
              - sucesso: bool
              - erro: se houve falha determinística no mapper
        """
        validacoes: list[dict] = []

        sistema = SistemaExterno.objects.filter(codigo=sistema_codigo).first()
        if not sistema:
            raise OperacaoNaoEncontrada(f'Sistema "{sistema_codigo}" não encontrado.')

        operacao = OperacaoIntegracao.objects.filter(
            sistema=sistema, codigo=operacao_codigo
        ).first()
        if not operacao:
            raise OperacaoNaoEncontrada(
                f'Operação "{operacao_codigo}" não configurada para {sistema.codigo}.'
            )

        # 1) Mapeamento REQUEST (canônico → schema externo)
        try:
            mapeamentos_req = list(
                MapeamentoCampo.objects.filter(
                    operacao=operacao, direcao=Direcao.REQUEST
                )
            )
            payload_mapeado = (
                mapear(payload, mapeamentos_req)
                if mapeamentos_req
                else deepcopy(payload)
            )
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro no mapeamento de REQUEST: {e}',
                'payload_entrada': payload,
                'validacoes': validacoes,
            }

        # 2) Validar campos obrigatórios manualmente (feedback detalhado)
        for m in mapeamentos_req:
            valor = _get_path(payload, m.origem_path, default=None)
            if valor is None and m.obrigatorio:
                validacoes.append({
                    'nivel': 'erro',
                    'campo_origem': m.origem_path,
                    'campo_destino': m.destino_path,
                    'mensagem': 'Campo obrigatório ausente no payload de entrada.',
                })
            elif valor is None and not m.obrigatorio:
                validacoes.append({
                    'nivel': 'aviso',
                    'campo_origem': m.origem_path,
                    'campo_destino': m.destino_path,
                    'mensagem': 'Campo ausente. Será usado o valor padrão.',
                    'valor_padrao': m.valor_padrao,
                })

        # 3) Resolver auth (ou pular)
        headers, params = {}, {}
        headers_auth_status = 'ignorada'
        if sistema.tipo_auth != 'NONE':
            if rodar_auth:
                try:
                    creds = decifrar(sistema.credenciais_cifradas)
                    auth_cls = obter_auth(sistema.tipo_auth)
                    headers, params = auth_cls(
                        sistema, creds, sistema.auth_extra
                    ).aplicar(headers, params)
                    headers_auth_status = 'executada'
                except Exception as e:
                    headers_auth_status = f'erro: {e}'
                    validacoes.append({
                        'nivel': 'erro',
                        'campo_origem': '_auth',
                        'mensagem': f'Falha na auth: {e}',
                    })
            else:
                headers_auth_status = 'pulada (use ?auth=true para testar)'

        # 4) Resolver adapter (só para saber qual seria usado)
        chave_adapter = sistema.adapter_customizado or sistema.protocolo
        try:
            obter_adapter(chave_adapter)
            adapter_resolvido = chave_adapter
        except KeyError as e:
            adapter_resolvido = f'ERRO: {e}'
            validacoes.append({
                'nivel': 'erro',
                'campo_origem': '_adapter',
                'mensagem': str(e),
            })

        # 5) Montar preview da request
        url_completa = (
            sistema.base_url.rstrip('/') + '/' + operacao.caminho.lstrip('/')
        )
        headers_finais = {**sistema.headers_padrao, **headers}
        if operacao.content_type:
            headers_finais.setdefault('Content-Type', operacao.content_type)
        headers_finais.setdefault('Accept', 'application/json')

        request_preview = {
            'metodo': operacao.metodo_http,
            'url': url_completa,
            'content_type': operacao.content_type,
            'headers': _mascarar_segredos(headers_finais),
            'params': params or {},
            'body': payload_mapeado,
            'timeout_segundos': sistema.timeout_segundos,
            'verify_ssl': sistema.verify_ssl,
            'adapter': adapter_resolvido,
            'auth_status': headers_auth_status,
            'adapter_params': operacao.adapter_params,
        }

        # 6) Se veio payload de resposta simulado, rodar mapper RESPONSE
        response_preview = None
        if payload_resposta_simulado is not None:
            mapeamentos_resp = list(
                MapeamentoCampo.objects.filter(
                    operacao=operacao, direcao=Direcao.RESPONSE
                )
            )
            try:
                response_preview = (
                    mapear(payload_resposta_simulado, mapeamentos_resp)
                    if mapeamentos_resp
                    else deepcopy(payload_resposta_simulado)
                )
            except Exception as e:
                validacoes.append({
                    'nivel': 'erro',
                    'campo_origem': '_response_mapper',
                    'mensagem': f'Erro ao mapear resposta simulada: {e}',
                })

        # 7) Registrar dry-run para auditoria (não afeta circuit breaker)
        tem_erro = any(v['nivel'] == 'erro' for v in validacoes)
        RegistroIntegracao.objects.create(
            sistema=sistema,
            operacao_codigo=operacao.codigo,
            direcao=Direcao.REQUEST,
            payload_original=payload,
            payload_mapeado=payload_mapeado,
            sucesso=not tem_erro,
            dry_run=True,
            erro='' if not tem_erro else 'Dry-run com erros de validação',
        )

        return {
            'sucesso': not tem_erro,
            'dry_run': True,
            'payload_entrada': payload,
            'payload_mapeado': payload_mapeado,
            'request_preview': request_preview,
            'response_preview': response_preview,
            'validacoes': validacoes,
        }

    # ========================================================================
    # EXECUÇÃO REAL
    # ========================================================================

    def executar(
        self,
        sistema_codigo: str,
        operacao_codigo: str,
        payload: dict,
        correlation_id=None,
    ) -> dict:
        correlation_id = correlation_id or uuid.uuid4()
        inicio = time.time()

        sistema = SistemaExterno.objects.filter(
            codigo=sistema_codigo, ativo=True
        ).first()
        if not sistema:
            raise OperacaoNaoEncontrada(
                f'Sistema "{sistema_codigo}" não encontrado ou inativo.'
            )

        if sistema.esta_bloqueado:
            raise SistemaBloqueado(
                f'Sistema "{sistema.codigo}" bloqueado até {sistema.bloqueado_ate}.'
            )

        operacao = OperacaoIntegracao.objects.filter(
            sistema=sistema, codigo=operacao_codigo, ativo=True
        ).first()
        if not operacao:
            raise OperacaoNaoEncontrada(
                f'Operação "{operacao_codigo}" não configurada para {sistema.codigo}.'
            )

        registro = RegistroIntegracao.objects.create(
            sistema=sistema,
            operacao_codigo=operacao.codigo,
            direcao=Direcao.REQUEST,
            payload_original=payload,
            correlation_id=correlation_id,
        )

        try:
            mapeamentos_req = MapeamentoCampo.objects.filter(
                operacao=operacao, direcao=Direcao.REQUEST
            )
            payload_mapeado = (
                mapear(payload, mapeamentos_req)
                if mapeamentos_req.exists()
                else payload
            )
            registro.payload_mapeado = payload_mapeado

            headers, params = {}, {}
            if sistema.tipo_auth != 'NONE':
                creds = decifrar(sistema.credenciais_cifradas)
                auth_cls = obter_auth(sistema.tipo_auth)
                headers, params = auth_cls(
                    sistema, creds, sistema.auth_extra
                ).aplicar(headers, params)

            chave_adapter = sistema.adapter_customizado or sistema.protocolo
            adapter_cls = obter_adapter(chave_adapter)
            adapter = adapter_cls(
                sistema=sistema,
                operacao=operacao,
                headers=headers,
                params=params,
                timeout=sistema.timeout_segundos,
                verify_ssl=sistema.verify_ssl,
            )

            resposta = adapter.executar(payload_mapeado)
            registro.resposta_bruta = resposta.corpo
            registro.status_code = resposta.status_code

            if resposta.status_code >= 400:
                if resposta.status_code == 429:
                    raise ErroRateLimit(f'HTTP 429: {resposta.corpo}')
                if resposta.status_code in (500, 502, 503, 504):
                    raise ErroTransiente(
                        f'HTTP {resposta.status_code}: {resposta.corpo}'
                    )
                raise ErroDefinitivo(
                    f'HTTP {resposta.status_code}: {resposta.corpo}'
                )

            mapeamentos_resp = MapeamentoCampo.objects.filter(
                operacao=operacao, direcao=Direcao.RESPONSE
            )
            resposta_mapeada = (
                mapear(resposta.corpo, mapeamentos_resp)
                if mapeamentos_resp.exists()
                else resposta.corpo
            )
            registro.resposta_mapeada = resposta_mapeada

            sistema.falhas_consecutivas = 0
            sistema.bloqueado_ate = None
            sistema.save(update_fields=['falhas_consecutivas', 'bloqueado_ate'])

            registro.sucesso = True
            registro.duracao_ms = int((time.time() - inicio) * 1000)
            registro.save()

            return {
                'sucesso': True,
                'dados': resposta_mapeada,
                'correlation_id': str(correlation_id),
                'duracao_ms': registro.duracao_ms,
            }

        except Exception as e:
            logger.exception(f'Falha em {sistema.codigo}.{operacao_codigo}')
            registro.sucesso = False
            registro.erro = str(e)
            registro.duracao_ms = int((time.time() - inicio) * 1000)
            registro.save()

            sistema.falhas_consecutivas += 1
            if sistema.falhas_consecutivas >= LIMITE_FALHAS:
                sistema.bloqueado_ate = timezone.now() + timedelta(
                    minutes=TEMPO_BLOQUEIO_MINUTOS
                )
            sistema.save(update_fields=['falhas_consecutivas', 'bloqueado_ate'])

            raise