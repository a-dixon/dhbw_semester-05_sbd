import os


def get_secret(path):
    ''' Read secret from file.'''
    # --- Check if file path exists ---
    existence = os.path.exists(path)
    # --- Read secret from file if exists ---
    if existence:
        with open(path, 'r') as f:
            return f.read()


SERVER_CERT = "config/certificates/server_certificates/server-public-key.pem"
SERVER_KEY = "config/certificates/server_certificates/server-private-key.pem"
CA_CERT = "config/certificates/root_ca/ca-public-key.pem"

INFLUX_URL = "http://10.0.1.30:8086"
INFLUX_TOKEN = "DzFwd-VxKfwt4Y20okuIDbolk3X8bcsGLOMDM0mp2IsdImr-Uji5JrclSyHmuUo-QLgIUmyQYJXzRhqKjNmmXQ=="
INFLUX_BUCKET = "smartmeter"
INFLUX_PROVIDER = "provider"


class MySQLConfig:
    ''' MySQL configuration class'''
    MYSQL_USER = 'provider'
    MYSQL_PASSWORD = get_secret('config/secrets/db_password.txt')
    MYSQL_HOST = '10.0.1.40'
    MYSQL_PORT = 3306

