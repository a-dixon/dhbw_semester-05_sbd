import os
from app.utils.certificates.pki_helpers import generate_csr, generate_private_key
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from app.utils.certificates.pki_helpers import sign_csr
from config import config


def generate_client_certificate(uid):
    output_folder = f"{config.CLIENT_CERT_DIRECTORY}/{uid}"
    os.makedirs(output_folder, exist_ok=True)  # Erstelle den Ordner, wenn er nicht existiert

    private_key_path = os.path.join(output_folder, "client-private-key.pem")
    csr_path = os.path.join(output_folder, "client-csr.pem")
    public_key_path = os.path.join(output_folder, "client-public-key.pem")

    server_private_key = generate_private_key(private_key_path)
    generate_csr(server_private_key, filename=csr_path, country="DE", state="Berlin", locality="Berlin", org="Trusty",
                 alt_dns=[], alt_ip=["10.0.1.20"], hostname=uid)

    csr_file = open(csr_path, "rb")
    csr = x509.load_pem_x509_csr(csr_file.read(), default_backend())

    ca_public_key_file = open("ca-public-key.pem", "rb")
    ca_public_key = x509.load_pem_x509_certificate(ca_public_key_file.read(), default_backend())

    ca_private_key_file = open("ca-private-key.pem", "rb")
    ca_private_key = serialization.load_pem_private_key(ca_private_key_file.read(), None, default_backend())

    sign_csr(csr, ca_public_key, ca_private_key, public_key_path)

    os.remove(csr_path)
