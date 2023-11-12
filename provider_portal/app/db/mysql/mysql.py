import sys
import mysql.connector
from mysql.connector import errorcode


class MySQL:
    def __init__(self):

        # --- Set connection data ---
        self._user = 'provider'
        self._password = 'xEMRpr32b7Xg8nNCWNakgnDrSja8b5'
        self._host = '10.0.1.40'
        self._port = 3306

        # --- Define DB name and tables ---
        self._DB_NAME = 'provider'

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

        # --- Create connector and cursor --- 
        self._cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        self._cursor = self._cnx.cursor()


        # --- Try to set DB name ---
        try:
            self._cursor.execute(f'USE {self._DB_NAME}')

        # --- Call create function if DB does not exist ---
        except mysql.connector.Error as err:
            print(f'Database {self._DB_NAME} does not exist.', file=sys.stderr)
            
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self._create_database(cursor=self._cursor)
                print(f'Database {self._DB_NAME} created successfully', file=sys.stderr)
                self._cnx.database = self._DB_NAME
            
            else:
                print(err)
                exit(1)

        # --- Create all tables ---
        for table_name in self._TABLES:
            table_description = self._TABLES[table_name]

            try:
                print(f'Creating table {table_name}:', end='', file=sys.stderr)
                self._cursor.execute(table_description)

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('already exists.', file=sys.stderr)

                else:
                    print(err.msg)

            else:
                print('OK', file=sys.stderr)

        self._cursor.close()
        self._cnx.close()
