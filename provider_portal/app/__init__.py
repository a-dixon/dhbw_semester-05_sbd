import sys
from flask import Flask
import mysql.connector
from mysql.connector import errorcode
#from config.config import MySQLConfig


def create_app():
   app = Flask(__name__)

   try:
      db = mysql.connector.connect(user='provider', password='xEMRpr32b7Xg8nNCWNakgnDrSja8b50',
                                host='10.0.1.40',
                                database='provider')
   except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
         print('Authentication error', file=sys.stderr)
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
         print('Database does not exist', file=sys.stderr)
      else:
         print(err, file=sys.stderr)
   else:
      db.close()


   from app.api.customer_api import customer_api_blueprint as customer_api_routes
   app.register_blueprint(customer_api_routes, url_prefix='/v1/provider')

   from app.api.smartmeter_api import smartmeter_api_blueprint as smartmeter_api_routes
   app.register_blueprint(smartmeter_api_routes, url_prefix='/v1/smartmeter')

   from app.api.admin_api import admin_api_blueprint as admin_api_routes
   app.register_blueprint(admin_api_routes, url_prefix='/v1/admin')

   return app
