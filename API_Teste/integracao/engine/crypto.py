# integracao/engine/crypto.py
import json
from cryptography.fernet import Fernet
from django.conf import settings


def _fernet():
    return Fernet(settings.INTEGRACAO_SECRET_KEY.encode())


def cifrar(dados: dict) -> bytes:
    return _fernet().encrypt(json.dumps(dados).encode())


def decifrar(blob: bytes) -> dict:
    if not blob:
        return {}
    return json.loads(_fernet().decrypt(bytes(blob)).decode())