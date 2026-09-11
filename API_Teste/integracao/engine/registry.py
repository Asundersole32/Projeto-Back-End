# integracao/engine/registry.py
"""
Registry de adapters, strategies de auth e transforms.

Todas as "peças plugáveis" do motor se registram aqui via decorators.
O engine resolve em runtime por chave — por isso o motor é um coringa:
não conhece nenhuma implementação concreta.
"""

from typing import Callable, Dict, Type


# ============================================================================
# Dicionários internos — registrados via decorators
# ============================================================================

_ADAPTERS: Dict[str, Type] = {}
_AUTH: Dict[str, Type] = {}
_AUTH_WEBHOOK: Dict[str, Type] = {}
_TRANSFORMS: Dict[str, Callable] = {}


# ============================================================================
# Decorators de registro
# ============================================================================

def registrar_adapter(chave: str):
    """Uso: @registrar_adapter('REST') acima da classe Adapter."""
    def deco(cls):
        _ADAPTERS[chave] = cls
        return cls
    return deco


def registrar_auth(chave: str):
    """Uso: @registrar_auth('BEARER') acima da classe AuthStrategy."""
    def deco(cls):
        _AUTH[chave] = cls
        return cls
    return deco


def registrar_auth_webhook(chave: str):
    """Uso: @registrar_auth_webhook('HMAC_SHA256') acima da WebhookAuthStrategy."""
    def deco(cls):
        _AUTH_WEBHOOK[chave] = cls
        return cls
    return deco


def registrar_transform(nome: str):
    """Uso: @registrar_transform('upper') acima da função de transformação."""
    def deco(fn):
        _TRANSFORMS[nome] = fn
        return fn
    return deco


# ============================================================================
# Resolução
# ============================================================================

def obter_adapter(chave: str) -> Type:
    if chave not in _ADAPTERS:
        raise KeyError(
            f'Adapter "{chave}" não registrado. '
            f'Disponíveis: {sorted(_ADAPTERS)}'
        )
    return _ADAPTERS[chave]


def obter_auth(chave: str) -> Type:
    if chave not in _AUTH:
        raise KeyError(
            f'Auth "{chave}" não registrada. '
            f'Disponíveis: {sorted(_AUTH)}'
        )
    return _AUTH[chave]


def obter_auth_webhook(chave: str) -> Type:
    if chave not in _AUTH_WEBHOOK:
        raise KeyError(
            f'Strategy de webhook "{chave}" não registrada. '
            f'Disponíveis: {sorted(_AUTH_WEBHOOK)}'
        )
    return _AUTH_WEBHOOK[chave]


def obter_transform(nome: str) -> Callable:
    if nome not in _TRANSFORMS:
        raise KeyError(
            f'Transform "{nome}" não registrada. '
            f'Disponíveis: {sorted(_TRANSFORMS)}'
        )
    return _TRANSFORMS[nome]


# ============================================================================
# Introspecção — endpoint /capacidades/
# ============================================================================

def listar_capacidades() -> dict:
    """Lista tudo que está registrado. Usado pelo endpoint /capacidades/."""
    return {
        'adapters': sorted(_ADAPTERS.keys()),
        'auth': sorted(_AUTH.keys()),
        'auth_webhook': sorted(_AUTH_WEBHOOK.keys()),
        'transforms': sorted(_TRANSFORMS.keys()),
    }