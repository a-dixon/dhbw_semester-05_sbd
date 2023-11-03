from flask import Flask


def create_app():
    app = Flask(__name__)

    from provider_portal.app.api.customer_api import routes as customer_api_routes
    app.register_blueprint(customer_api_routes, url_prefix='/v1/provider')

    return app