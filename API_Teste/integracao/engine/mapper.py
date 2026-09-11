# integracao/engine/mapper.py
from typing import Any
from jsonpath_ng.ext import parse as jsonpath_parse
from .registry import obter_transform


def _get_path(data: Any, path: str, default=None):
    """Suporta JSONPath ($.a.b) ou dot-notation (a.b)."""
    if path.startswith('$'):
        matches = jsonpath_parse(path).find(data)
        return matches[0].value if matches else default
    # dot notation
    cur = data
    for parte in path.split('.'):
        if isinstance(cur, dict) and parte in cur:
            cur = cur[parte]
        elif isinstance(cur, list) and parte.isdigit():
            cur = cur[int(parte)]
        else:
            return default
    return cur


def _set_path(data: dict, path: str, value: Any):
    partes = path.split('.')
    cur = data
    for p in partes[:-1]:
        cur = cur.setdefault(p, {})
    cur[partes[-1]] = value


def aplicar_transformacoes(valor, transformacoes: list):
    for t in transformacoes or []:
        fn = obter_transform(t['nome'])
        valor = fn(valor, **(t.get('params') or {}))
    return valor


def mapear(payload_origem: dict, mapeamentos) -> dict:
    """
    `mapeamentos` é um iterável de objetos MapeamentoCampo (com .origem_path, .destino_path,
    .transformacoes, .valor_padrao, .obrigatorio).
    """
    destino = {}
    for m in mapeamentos:
        valor = _get_path(payload_origem, m.origem_path, default=None)
        if valor is None:
            if m.obrigatorio and m.valor_padrao is None:
                raise ValueError(f'Campo obrigatório ausente: {m.origem_path}')
            valor = m.valor_padrao
        if valor is not None:
            valor = aplicar_transformacoes(valor, m.transformacoes)
        _set_path(destino, m.destino_path, valor)
    return destino