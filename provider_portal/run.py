import ssl
import sys
import threading
import time
import logging
from flask import Flask
from app.db.mysql import mysql
from config import config
from app.utils.init.create_admin_users import insert_users_from_file

# Enable Logging
logging.basicConfig(level=config.LoggingConfig.LOGGING_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("main")
file_handler = logging.FileHandler(config.LoggingConfig.LOGGING_FILE)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Flask applications
customer_api_app = Flask(__name__)
from app.api.customer_api import customer_api_blueprint as customer_api_routes

customer_api_app.register_blueprint(customer_api_routes, url_prefix="/v1/provider")

smartmeter_api_app = Flask(__name__)
from app.api.smartmeter_api import smartmeter_api_blueprint as smartmeter_api_routes

smartmeter_api_app.register_blueprint(smartmeter_api_routes, url_prefix="/v1/smartmeter")

admin_api_app = Flask(__name__)
from app.api.admin_api import admin_api_blueprint as admin_api_routes

admin_api_app.register_blueprint(admin_api_routes, url_prefix="/v1/admin")

log = logging.getLogger("werkzeug")
log.disabled = True


def run_app(app, host, port, ssl_context):
    try:
        app.run(host=host, port=port, ssl_context=ssl_context)
    except Exception as e:
        logger.error(f"Error running {app.name}: {e}")


if __name__ == '__main__':
    # SSL context setup
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=config.CertificateConfig.SERVER_CERT,
                                keyfile=config.CertificateConfig.SERVER_KEY)
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.load_verify_locations(cafile=config.CertificateConfig.CA_CERT)

    # MySQL database setup
    mysql_db = mysql.MySQL()

    while True:
        try:
            # Attempt to connect to the database
            mysql_db.create()
            logger.info("The application has successfully connected to the database.")
            break
        except Exception as err:
            # Handle database connection errors
            logger.error(f"The following error occurred when connecting to the database: {err}")
            logger.info("A new attempt is made in 5 seconds.")
            time.sleep(5)

    # Initialize admin users from file
    if config.InitAdminUsers.ADMIN_INIT_ACTIVATED:
        insert_users_from_file(mysql_db)

    # Threaded Flask applications
    smartmeter_thread = threading.Thread(target=run_app, args=(smartmeter_api_app, '10.0.1.10', 8080, ssl_context))
    smartmeter_thread.start()

    provider_thread = threading.Thread(target=run_app, args=(
    customer_api_app, '10.0.1.10', 443, (config.CertificateConfig.SERVER_CERT, config.CertificateConfig.SERVER_KEY)))
    provider_thread.start()

    admin_thread = threading.Thread(target=run_app, args=(
    admin_api_app, '10.0.1.10', 8090, (config.CertificateConfig.SERVER_CERT, config.CertificateConfig.SERVER_KEY)))
    admin_thread.start()

    # Wait for all threads to finish
    smartmeter_thread.join()
    provider_thread.join()
    admin_thread.join()
