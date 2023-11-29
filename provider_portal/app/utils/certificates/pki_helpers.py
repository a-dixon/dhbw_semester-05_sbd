from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta
import ipaddress


def generate_private_key(filename: str) -> rsa.RSAPrivateKey:
    """
    Generate an RSA private key and save it to a file.

    Args:
        filename (str): The name of the file to save the private key.

    Returns:
        rsa.RSAPrivateKey: The generated RSA private key.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    with open(filename, "wb") as keyfile:
        keyfile.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    return private_key


def generate_public_key(
    private_key: rsa.RSAPrivateKey, filename: str, **kwargs
) -> x509.Certificate:
    """
    Generate a self-signed public key (X.509 certificate) and save it to a file.

    Args:
        private_key (rsa.RSAPrivateKey): The private key corresponding to the public key.
        filename (str): The name of the file to save the public key.
        **kwargs: Additional information for the certificate.

    Returns:
        x509.Certificate: The generated X.509 certificate.
    """
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, kwargs["country"]),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, kwargs["state"]),
            x509.NameAttribute(NameOID.LOCALITY_NAME, kwargs["locality"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, kwargs["org"]),
            x509.NameAttribute(NameOID.COMMON_NAME, kwargs["hostname"]),
        ]
    )

    # Because this is self-signed, the issuer is always the subject
    issuer = subject

    # This certificate is valid from now until 30 days
    valid_from = datetime.utcnow()
    valid_to = valid_from + timedelta(days=30)

    # Used to build the certificate
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_to)
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
    )

    # Sign the certificate with the private key
    public_key = builder.sign(private_key, hashes.SHA256(), default_backend())

    with open(filename, "wb") as certfile:
        certfile.write(public_key.public_bytes(serialization.Encoding.PEM))

    return public_key


def generate_csr(
    private_key: rsa.RSAPrivateKey, filename: str, **kwargs
) -> x509.CertificateSigningRequest:
    """
    Generate a Certificate Signing Request (CSR) and save it to a file.

    Args:
        private_key (rsa.RSAPrivateKey): The private key corresponding to the CSR.
        filename (str): The name of the file to save the CSR.
        **kwargs: Additional information for the CSR.

    Returns:
        x509.CertificateSigningRequest: The generated CSR.
    """
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, kwargs["country"]),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, kwargs["state"]),
            x509.NameAttribute(NameOID.LOCALITY_NAME, kwargs["locality"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, kwargs["org"]),
            x509.NameAttribute(NameOID.COMMON_NAME, kwargs["hostname"]),
        ]
    )

    # Generate any alternative DNS names
    alt_names = [
        x509.DNSName(name) for name in kwargs.get("alt_dns", [])
    ] + [
        x509.IPAddress(ipaddress.IPv4Address(name))
        for name in kwargs.get("alt_ip", [])
    ]
    san = x509.SubjectAlternativeName(alt_names)

    builder = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(subject)
        .add_extension(san, critical=False)
    )

    csr = builder.sign(private_key, hashes.SHA256(), default_backend())

    with open(filename, "wb") as csrfile:
        csrfile.write(csr.public_bytes(serialization.Encoding.PEM))

    return csr


def sign_csr(
    csr: x509.CertificateSigningRequest,
    ca_public_key: x509.Certificate,
    ca_private_key: rsa.RSAPrivateKey,
    new_filename: str,
) -> x509.Certificate:
    """
    Sign a Certificate Signing Request (CSR) with a Certificate Authority's key pair.

    Args:
        csr (x509.CertificateSigningRequest): The CSR to be signed.
        ca_public_key (x509.Certificate): The public key of the Certificate Authority.
        ca_private_key (rsa.RSAPrivateKey): The private key of the Certificate Authority.
        new_filename (str): The name of the file to save the signed certificate.

    Returns:
        x509.Certificate: The signed certificate.
    """
    valid_from = datetime.utcnow()
    valid_until = valid_from + timedelta(days=1800)

    builder = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_public_key.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_until)
    )

    for extension in csr.extensions:
        builder = builder.add_extension(extension.value, extension.critical)

    public_key = builder.sign(
        private_key=ca_private_key, algorithm=hashes.SHA256(), backend=default_backend()
    )

    with open(new_filename, "wb") as keyfile:
        keyfile.write(public_key.public_bytes(serialization.Encoding.PEM))