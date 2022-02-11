from __future__ import annotations

import datetime
import random
import time
from os import PathLike
from pathlib import Path
from typing import Any

import aiofiles
import orjson
from cryptography import x509
from cryptography.hazmat._oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import Request


def camel(snake: str) -> str:
    first, *rest = snake.split("_")
    return first + "".join(s.capitalize() for s in rest)


def pascal(snake: str) -> str:
    return "".join(s.capitalize() for s in snake.split("_"))


def underscore_prefix(snake: str) -> str:
    return "_" + snake


def timestamp() -> int:
    return int(time.time())


def server_url(request: Request) -> str:
    return f"https://{request.base_url.hostname}:443"


async def read_json_file(path: PathLike[str]) -> Any:
    async with aiofiles.open(path, encoding="utf8") as file:
        return orjson.loads(await file.read())


def generate_id() -> str:
    return "".join(random.choices("0123456789abcdef", k=24))


def generate_certificates(directory: Path) -> None:
    key_path = directory.joinpath("key.pem")
    cert_path = directory.joinpath("certificate.pem")

    if key_path.exists() and cert_path.exists():
        return

    key = rsa.generate_private_key(public_exponent=0x10001, key_size=2048)
    bytes_ = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b" "),
    )

    with key_path.open("wb") as file:
        file.write(bytes_)

    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, ""),
            x509.NameAttribute(NameOID.LOCALITY_NAME, ""),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, ""),
            x509.NameAttribute(NameOID.COMMON_NAME, ""),
        ]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365 * 42))
        .sign(key, hashes.SHA256())
    )
    with cert_path.open("wb") as file:
        file.write(cert.public_bytes(serialization.Encoding.PEM))
