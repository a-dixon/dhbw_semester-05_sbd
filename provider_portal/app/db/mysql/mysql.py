import sys
import mysql.connector
from mysql.connector import errorcode
from config.config import MySQLConfig


class MySQL:
    def __init__(self):

        # --- Load config data ---
        self._user = MySQLConfig.MYSQL_USER
        self._password = MySQLConfig.MYSQL_PASSWORD
        self._host = MySQLConfig.MYSQL_HOST
        self._port = MySQLConfig.MYSQL_PORT
        self._DB_NAME = 'provider'

    def _create_database(self, cursor):
        ''' Create database.'''
        try:
            cursor.execute(
                f'CREATE DATABASE {self._DB_NAME} DEFAULT CHARACTER SET "utf8"')
            
        except mysql.connector.Error as err:
                print(f'Failed creating database: {err}', file=sys.stderr)
                exit(1)


    def create(self):
        ''' Create database and tables.'''

        self._TABLES = {}
        self._TABLES['customers'] = (
            "CREATE TABLE `customers` ("
            "   `customer_UID` varchar(36) NOT NULL,"
            "   `api_key` varchar(32) NOT NULL,"
            "   PRIMARY KEY (`customer_UID`)"
            ") ENGINE=InnoDB")

        self._TABLES['meters'] = (
            "CREATE TABLE `meters`("
            "   `meter_UID` varchar(36) NOT NULL,"
            "   PRIMARY KEY (`meter_UID`)"
            ") ENGINE=InnoDB")

        self._TABLES['customers_meters'] = (
            "CREATE TABLE `customers_meters` ("
            "   `customer_UID` varchar(36) NOT NULL,"
            "   `meter_UID` varchar(36) NOT NULL,"
            "   PRIMARY KEY (`customer_UID`,`meter_UID`),"
            "   KEY `customer_UID` (`customer_UID`),"
            "   KEY `meters_UID` (`meter_UID`),"
            "   CONSTRAINT `customers_meters_fk_1` FOREIGN KEY (`customer_UID`)"
            "       REFERENCES `customers` (`customer_UID`) ON DELETE CASCADE,"
            "   CONSTRAINT `customers_meters_fk_2` FOREIGN KEY (`meter_UID`)"
            "       REFERENCES `meters` (`meter_UID`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        self._TABLES['users'] = (
            "CREATE TABLE `users`("
            "   `user_UID` varchar(36) NOT NULL,"
            "   `api_key` varchar(32) NOT NULL,"
            "   `username` varchar(32)"
            ") ENGINE=InnoDB")

        # --- Create connector and cursor --- 
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor()

        # --- Try to set DB name ---
        try:
            cursor.execute(f'USE {self._DB_NAME}')

        # --- Call create function if DB does not exist ---
        except mysql.connector.Error as err:
            print(f'Database {self._DB_NAME} does not exist.', file=sys.stderr)
            
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self._create_database(cursor=cursor)
                print(f'Database {self._DB_NAME} created successfully', file=sys.stderr)
                cnx.database = self._DB_NAME
            
            else:
                print(err)
                exit(1)

        # --- Create all tables ---
        for table_name in self._TABLES:
            table_description = self._TABLES[table_name]

            try:
                print(f'Creating table {table_name}:', end='', file=sys.stderr)
                cursor.execute(table_description)

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print(' already exists.', file=sys.stderr)

                else:
                    print(err.msg)

            else:
                print(' OK', file=sys.stderr)

        cursor.close()
        cnx.close()

    
    def insert_test_data(self):
        # --- Create connector and cursor --- 
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor()
        cnx.database = self._DB_NAME

        customer_UID_1 = '123456'
        customer_api_key_1 = 'abcdefg'

        customer_UID_2 = '654321'
        customer_api_key_2 = 'gfedcba'

        add_customer_1 = (f'INSERT INTO customers (customer_UID, api_key) VALUES ("{customer_UID_1}", "{customer_api_key_1}")')
        add_customer_2 = (f'INSERT INTO customers (customer_UID, api_key) VALUES ("{customer_UID_2}", "{customer_api_key_2}")')

        cursor.execute(add_customer_1)
        cursor.execute(add_customer_2)

        cnx.commit()

        cursor.close()
        cnx.close()

    
    def get_api_key(self, customer_UID: str):
        ''' Returns API Key for corresponding customer UID.'''

        # --- Create connector and cursor --- 
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor(buffered=True)
        cnx.database = self._DB_NAME

        # --- Query database ---
        query = (f'SELECT api_key FROM customers WHERE customer_UID="{customer_UID}"')
        cursor.execute(query)
        api_key = cursor.fetchone()[0]

        # --- Cleanup ---
        cursor.close()
        cnx.close()

        return api_key
    

    def _insert_meter(self, meter_UID: str):
        ''' Insert meter_UID into meters table.'''
        # --- Create connector and cursor --- 
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor(buffered=True)
        cnx.database = self._DB_NAME

        # --- Query database ---
        query = (f'INSERT INTO meters (meter_UID) VALUES ("{meter_UID}")')
        cursor.execute(query)
        cnx.commit()

        # --- Cleanup --- 
        cursor.close()
        cnx.close()


    def _insert_customer_meter(self, customer_UID: str, meter_UID: str):
        ''' Insert customer_UID and meter_UID into customers_meters table.'''
        # --- Create connector and cursor --- 
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor(buffered=True)
        cnx.database = self._DB_NAME

        # --- Query database ---
        query = (f'INSERT INTO customers_meters (customer_UID, meter_UID) VALUES ("{customer_UID}", "{meter_UID}")')
        cursor.execute(query)
        cnx.commit()

        # --- Cleanup ---
        cursor.close()
        cnx.close()


    def delete_customer_meter(self, meter_UID: str):
        ''' Delete entry for meter_UID in customers_meters table.'''
        # --- Create connector and cursor --- 
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor(buffered=True)
        cnx.database = self._DB_NAME

        # --- Query database ---
        query = (f'DELETE FROM customers_meters WHERE meter_UID = "{meter_UID}"')
        cursor.execute(query)
        cnx.commit()

        # --- Cleanup ---
        cursor.close()
        cnx.close()

    def delete_meter(self, meter_UID: str):
        ''' Delete entry for meter_UID in meters table.'''
        # --- Create connector and cursor --- 
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor(buffered=True)
        cnx.database = self._DB_NAME

        # --- Query database ---
        query = f'DELETE FROM meters WHERE meter_UID = "{meter_UID}"'
        cursor.execute(query)

        # Check the affected row count
        affected_rows = cursor.rowcount

        # Commit the changes
        cnx.commit()

        # --- Cleanup ---
        cursor.close()
        cnx.close()

        # Raise an error if no rows were affected
        if affected_rows == 0:
            raise ValueError(f"No meter found with meter_UID: {meter_UID}.")
