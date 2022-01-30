import datetime
from pathlib import Path

from cryptography import x509
from cryptography.hazmat._oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_certificates(directory: Path) -> None:
    key = rsa.generate_private_key(public_exponent=0x10001, key_size=2048)
    bytes_ = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b" "),
    )

    with directory.joinpath("key.pem").open("wb") as file:
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
    with directory.joinpath("certificate.pem").open("wb") as file:
        file.write(cert.public_bytes(serialization.Encoding.PEM))
