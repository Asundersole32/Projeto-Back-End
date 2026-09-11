# integracao/transforms/builtin.py
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from ..engine.registry import registrar_transform


@registrar_transform('upper')
def upper(v, **_):
    return str(v).upper() if v is not None else v


@registrar_transform('lower')
def lower(v, **_):
    return str(v).lower() if v is not None else v


@registrar_transform('strip')
def strip(v, **_):
    return str(v).strip() if v is not None else v


@registrar_transform('decimal')
def decimal(v, casas=2, **_):
    try:
        return float(Decimal(str(v)).quantize(Decimal('1.' + '0' * casas)))
    except (InvalidOperation, TypeError):
        return None


@registrar_transform('date_format')
def date_format(v, de='%Y-%m-%d', para='%d/%m/%Y', **_):
    if not v:
        return None
    for fmt in (de, '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%SZ'):
        try:
            dt = datetime.strptime(str(v), fmt)
            return dt.strftime(para)
        except ValueError:
            continue
    return v


@registrar_transform('lookup')
def lookup(v, tabela=None, default=None, **_):
    """tabela = {valor_origem: valor_destino}"""
    if not tabela:
        return v
    return tabela.get(str(v), default if default is not None else v)


@registrar_transform('default')
def default(v, valor=None, **_):
    return v if v not in (None, '', []) else valor


@registrar_transform('split')
def split(v, sep=',', index=0, **_):
    partes = str(v).split(sep)
    try:
        return partes[index]
    except IndexError:
        return None


@registrar_transform('template')
def template(v, padrao='{v}', **_):
    return padrao.format(v=v)