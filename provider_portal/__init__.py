from flask import Flask


def create_app():
    # Create flask app
    app = Flask(__name__)

    # Register API blueprint
    from provider_portal.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


    return app