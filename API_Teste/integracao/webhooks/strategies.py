# integracao/webhooks/strategies.py
import hmac
import hashlib
import time
from .base import WebhookAuthStrategy, ResultadoValidacao
from ..engine.registry import registrar_auth_webhook  # ver registry atualizado


def _comparar(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode(), b.encode())


def _calcular_hmac(segredo: str, mensagem: bytes, algoritmo: str = 'sha256') -> str:
    return hmac.new(segredo.encode(), mensagem, getattr(hashlib, algoritmo)).hexdigest()


def _verificar_com_segredos(segredos: dict, mensagem: bytes, assinatura: str,
                             algoritmo: str = 'sha256') -> bool:
    """Testa com segredo atual e anterior (rotação)."""
    candidatos = [segredos.get('atual'), segredos.get('anterior')]
    for seg in candidatos:
        if not seg:
            continue
        esperado = _calcular_hmac(seg, mensagem, algoritmo)
        if _comparar(esperado, assinatura):
            return True
    return False


@registrar_auth_webhook('HMAC_SHA256')
class HmacSha256Strategy(WebhookAuthStrategy):
    """
    Estratégia genérica:
      - Header com assinatura (default: X-Signature)
      - Timestamp em header separado (default: X-Timestamp)
      - HMAC-SHA256 sobre `timestamp + '.' + body_bruto`
      - Tolerância configurável
    """

    def validar(self, request):
        header_sig = self.params.get('header_signature', 'X-Signature')
        header_ts = self.params.get('header_timestamp', 'X-Timestamp')

        assinatura = request.headers.get(header_sig, '')
        ts_raw = request.headers.get(header_ts, '')

        if not assinatura:
            return ResultadoValidacao(False, f'Header {header_sig} ausente')

        if ts_raw:
            try:
                ts = int(ts_raw)
            except ValueError:
                return ResultadoValidacao(False, 'Timestamp inválido')
            tolerancia = self.sistema.webhook_tolerancia_segundos
            if abs(time.time() - ts) > tolerancia:
                return ResultadoValidacao(False, f'Timestamp fora da tolerância ({tolerancia}s)')
            mensagem = f'{ts}.'.encode() + request.body
        else:
            ts = None
            mensagem = request.body

        if not _verificar_com_segredos(self.segredos, mensagem, assinatura, 'sha256'):
            return ResultadoValidacao(False, 'Assinatura HMAC inválida')

        delivery_id = (
            request.headers.get('X-Delivery-ID')
            or request.headers.get('X-Event-ID')
            or ''
        )
        return ResultadoValidacao(True, delivery_id=delivery_id, timestamp=ts)


@registrar_auth_webhook('GITHUB')
class GithubWebhookStrategy(WebhookAuthStrategy):
    """
    Padrão GitHub: header X-Hub-Signature-256: sha256=<hex>
    Assina só o corpo (sem timestamp).
    """

    def validar(self, request):
        raw = request.headers.get('X-Hub-Signature-256', '')
        if not raw.startswith('sha256='):
            return ResultadoValidacao(False, 'Header X-Hub-Signature-256 ausente ou malformado')
        assinatura = raw[len('sha256='):]
        if not _verificar_com_segredos(self.segredos, request.body, assinatura, 'sha256'):
            return ResultadoValidacao(False, 'Assinatura GitHub inválida')
        delivery_id = request.headers.get('X-GitHub-Delivery', '')
        return ResultadoValidacao(True, delivery_id=delivery_id)


@registrar_auth_webhook('STRIPE')
class StripeWebhookStrategy(WebhookAuthStrategy):
    """
    Padrão Stripe: header 'Stripe-Signature: t=<ts>,v1=<hex>'
    Assina: f'{t}.{body}'
    """

    def validar(self, request):
        raw = request.headers.get('Stripe-Signature', '')
        if not raw:
            return ResultadoValidacao(False, 'Header Stripe-Signature ausente')

        partes = dict(p.split('=', 1) for p in raw.split(',') if '=' in p)
        ts_str = partes.get('t')
        assinatura = partes.get('v1')
        if not ts_str or not assinatura:
            return ResultadoValidacao(False, 'Stripe-Signature malformado')

        ts = int(ts_str)
        if abs(time.time() - ts) > self.sistema.webhook_tolerancia_segundos:
            return ResultadoValidacao(False, 'Timestamp fora da tolerância')

        mensagem = f'{ts}.'.encode() + request.body
        if not _verificar_com_segredos(self.segredos, mensagem, assinatura, 'sha256'):
            return ResultadoValidacao(False, 'Assinatura Stripe inválida')

        return ResultadoValidacao(True, timestamp=ts)


@registrar_auth_webhook('HMAC_SHA1')
class HmacSha1Strategy(WebhookAuthStrategy):
    """Para sistemas legados (TOTVS antigo, alguns ERPs)."""

    def validar(self, request):
        header_sig = self.params.get('header_signature', 'X-Signature')
        assinatura = request.headers.get(header_sig, '')
        if not assinatura:
            return ResultadoValidacao(False, f'Header {header_sig} ausente')
        if not _verificar_com_segredos(self.segredos, request.body, assinatura, 'sha1'):
            return ResultadoValidacao(False, 'Assinatura HMAC-SHA1 inválida')
        return ResultadoValidacao(True)


@registrar_auth_webhook('NONE')
class NoAuthStrategy(WebhookAuthStrategy):
    """Só para desenvolvimento/teste. NUNCA em produção."""

    def validar(self, request):
        return ResultadoValidacao(True, motivo='Sem validação (NONE)')