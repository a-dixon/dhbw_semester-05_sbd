

SERVER_CERT = "provider_portal/config/certificates/server_certificates/server-public-key.pem"
SERVER_KEY = "provider_portal/config/certificates/server_certificates/server-private-key.pem"
CA_CERT = "provider_portal/config/certificates/root_ca/ca-public-key.pem"

class MySQLConfig(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://provider_user:db_password@mysql/provider_db'
