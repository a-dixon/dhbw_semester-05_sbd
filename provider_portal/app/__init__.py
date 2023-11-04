from flask import Flask


def create_app():
    app = Flask(__name__)

    from provider_portal.app.api.customer_api import customer_api_blueprint as customer_api_routes
    app.register_blueprint(customer_api_routes, url_prefix='/v1/provider')

    from provider_portal.app.api.smartmeter_api import smartmeter_api_blueprint as smartmeter_api_routes
    app.register_blueprint(smartmeter_api_routes, url_prefix='/v1/smartmeter')

    from provider_portal.app.api.admin_api import admin_api_blueprint as admin_api_routes
    app.register_blueprint(admin_api_routes, url_prefix='/v1/smartmeter')

    return app