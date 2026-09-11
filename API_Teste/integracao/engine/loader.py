# integracao/engine/loader.py
from importlib.metadata import entry_points


def carregar_plugins():
    for ep in entry_points(group='integracao.adapters'):
        ep.load()  # importa o módulo, que se auto-registra via decorator