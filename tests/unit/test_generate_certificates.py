from pathlib import Path

from utils import generate_certificates


def test_creates_two_certificate_files(tmpdir):
    generate_certificates(Path(tmpdir))
    assert tmpdir.join("certificate.pem").exists()
    assert tmpdir.join("key.pem").exists()
