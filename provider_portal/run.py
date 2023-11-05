import os
import ssl

import werkzeug
import OpenSSL
from flask_sqlalchemy import SQLAlchemy

from provider_portal.config import config

from app import create_app
from provider_portal.config.config import MySQLConfig


ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile=config.CA_CERT)
ssl_context.load_cert_chain(certfile=config.SERVER_CERT, keyfile=config.SERVER_KEY)
ssl_context.verify_mode = ssl.CERT_REQUIRED


class PeerCertWSGIRequestHandler(werkzeug.serving.WSGIRequestHandler):
    def make_environ(self):
        environ = super(PeerCertWSGIRequestHandler, self).make_environ()
        x509_binary = self.connection.getpeercert(True)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, x509_binary)
        environ['peercert'] = x509
        return environ


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080, ssl_context=ssl_context, request_handler=PeerCertWSGIRequestHandler)
