from flask import Flask
from config.config import MySQLConfig
from flask_sqlalchemy import SQLAlchemy


def create_app():
   app = Flask(__name__)
   global mysql_db
   mysql_db = SQLAlchemy(app)
   app.config.from_object(MySQLConfig)

   from app.db.mysql import mysql

   with app.app_context():
      mysql_db.create_all()

   from app.api.customer_api import customer_api_blueprint as customer_api_routes
   app.register_blueprint(customer_api_routes, url_prefix='/v1/provider')

   from app.api.smartmeter_api import smartmeter_api_blueprint as smartmeter_api_routes
   app.register_blueprint(smartmeter_api_routes, url_prefix='/v1/smartmeter')

   from app.api.admin_api import admin_api_blueprint as admin_api_routes
   app.register_blueprint(admin_api_routes, url_prefix='/v1/admin')

   return app
