import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from app.utils.certificates.pki_helpers import generate_csr, generate_private_key, sign_csr
from config import config


def generate_client_certificate(uid):
    """
    Generate a client certificate for the given user identifier.

    Args:
        uid (str): User identifier of smartmeter.

    Returns:
        None
    """
    output_folder = f"{config.CertificateConfig.CLIENT_CERT_DIRECTORY}/{uid}"
    os.makedirs(output_folder, exist_ok=True)

    private_key_path = os.path.join(output_folder, "client-private-key.pem")
    csr_path = os.path.join(output_folder, "client-csr.pem")
    public_key_path = os.path.join(output_folder, "client-public-key.pem")

    server_private_key = generate_private_key(private_key_path)
    generate_csr(server_private_key, filename=csr_path, country="DE", state="Berlin", locality="Berlin", org="Trusty",
                 alt_dns=[], alt_ip=["127.0.0.1", "128.140.89.189", "10.0.1.10", "10.0.1.30", "10.0.1.40"], hostname=uid)

    with open(csr_path, "rb") as csr_file:
        csr = x509.load_pem_x509_csr(csr_file.read(), default_backend())

    with open(config.CertificateConfig.CA_PUBLIC_CERT, "rb") as ca_public_key_file:
        ca_public_key = x509.load_pem_x509_certificate(ca_public_key_file.read(), default_backend())

    with open(config.CertificateConfig.CA_PRIVATE_CERT, "rb") as ca_private_key_file:
        ca_private_key = serialization.load_pem_private_key(ca_private_key_file.read(), None, default_backend())

    sign_csr(csr, ca_public_key, ca_private_key, public_key_path)

    os.remove(csr_path)