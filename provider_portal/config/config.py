

SERVER_CERT = "provider_portal/config/certificates/server_certificates/server-public-key.pem"
SERVER_KEY = "provider_portal/config/certificates/server_certificates/server-private-key.pem"
CA_CERT = "provider_portal/config/certificates/root_ca/ca-public-key.pem"

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://provider_user:db_password@mysql/provider_db'
