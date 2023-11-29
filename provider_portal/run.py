import ssl
import sys
import threading
import time

from config import config
from flask import Flask
from app.db.mysql import mysql

customer_api_app = Flask(__name__)
from app.api.customer_api import customer_api_blueprint as customer_api_routes
customer_api_app.register_blueprint(customer_api_routes, url_prefix='/v1/provider')

smartmeter_api_app = Flask(__name__)
from app.api.smartmeter_api import smartmeter_api_blueprint as smartmeter_api_routes
smartmeter_api_app.register_blueprint(smartmeter_api_routes, url_prefix='/v1/smartmeter')

admin_api_app = Flask(__name__)
from app.api.admin_api import admin_api_blueprint as admin_api_routes
admin_api_app.register_blueprint(admin_api_routes, url_prefix='/v1/admin')


def run_app(app, host, port, ssl_context):
    app.run(host=host, port=port, ssl_context=ssl_context)
    return app


if __name__ == '__main__':
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile=config.CertificateConfig.CA_CERT)
    ssl_context.load_cert_chain(certfile=config.CertificateConfig.SERVER_CERT, keyfile=config.CertificateConfig.SERVER_KEY)
    ssl_context.verify_mode = ssl.CERT_REQUIRED

    mysql_db = mysql.MySQL()

    while True:
        try:
            mysql_db.create()
            print(f"The application has successfully connected to the database.", file=sys.stderr)
            break
        except Exception as err:
            print(f"The following error occurred when connecting to the database: {err}", file=sys.stderr)
            print(f"A new attempt is made in 5 seconds.", file=sys.stderr)
            time.sleep(5)

    smartmeter_thread = threading.Thread(target=run_app, args=(smartmeter_api_app, '10.0.1.10', 8080, ssl_context))
    smartmeter_thread.start()

    provider_thread = threading.Thread(target=run_app, args=(customer_api_app, '10.0.1.10', 443, (config.CertificateConfig.SERVER_CERT, config.CertificateConfig.SERVER_KEY)))
    provider_thread.start()

    admin_thread = threading.Thread(target=run_app, args=(admin_api_app, '10.0.1.10', 8090, (config.CertificateConfig.SERVER_CERT, config.CertificateConfig.SERVER_KEY)))
    admin_thread.start()

    smartmeter_thread.join()
    provider_thread.join()
    admin_thread.join()