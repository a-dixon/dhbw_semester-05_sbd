import os


def get_secret(path):
    ''' Read secret from file.'''
    # --- Check if file path exists ---
    existence = os.path.exists(path)
    # --- Read secret from file if exists ---
    if existence:
        with open(path, 'r') as f:
            return f.read()

class MySQLConfig:
    ''' MySQL configuration class'''
    MYSQL_USER = 'provider'
    MYSQL_PASSWORD = get_secret('config/secrets/db_password.txt')
    MYSQL_HOST = '10.0.1.40'
    MYSQL_PORT = 3306

class InfluxConfig:
    ''' InfluxDB configuration class'''
    INFLUX_URL = "http://10.0.1.30:8086"
    INFLUX_TOKEN = get_secret("config/secrets/influx_token.txt")
    INFLUX_BUCKET = "smartmeter"
    INFLUX_PROVIDER = "provider"

class CertificateConfig:
    ''' Certificate configuration class'''
    SERVER_CERT = "config/certificates/server_certificates/server-public-key.pem"
    SERVER_KEY = "config/certificates/server_certificates/server-private-key.pem"
    CA_PUBLIC_CERT = "config/certificates/root_ca/ca-public-key.pem"
    CA_PRIVATE_CERT = "config/certificates/root_ca/ca-private-key.pem"
    CA_CERT = "config/certificates/root_ca/ca-public-key.pem"
    CLIENT_CERT_DIRECTORY = "/app/smart_meter/config/certificates/smartmeter_certificates"



