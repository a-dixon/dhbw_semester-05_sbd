class CertificateConfig:
    """
    Configuration class for smart meter certificates.
    """
    CERT_DIRECTORY = "config/certificates/smartmeter_certificates"
    ROOT_CA_PEM = "config/certificates/root_ca/ca-public-key.pem"

class APIConfig:
    """
    Configuration class for the API.
    """
    API_URL = "https://10.0.1.10:8080/v1/smartmeter/meter-measurements"

class SmartmeterConfig:
    """
    Configuration class for smart meter details.
    """
    AVERAGE_CONSUMPTION_PER_YEAR = 200000  # kwh per smart meter per year
    RANDOMNESS_FACTOR = 1  # value between 0 and 1


