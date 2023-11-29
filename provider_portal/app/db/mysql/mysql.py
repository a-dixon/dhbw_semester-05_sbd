import sys
import mysql.connector
from mysql.connector import errorcode
from config.config import MySQLConfig


class MySQL:
    """
    A class for interacting with MySQL databases, creating tables, and performing CRUD operations.
    """

    def __init__(self):
        """
        Initializes the MySQL class with configuration data for connecting to the MySQL database.
        """
        # Load configuration data
        self._user = MySQLConfig.MYSQL_USER
        self._password = MySQLConfig.MYSQL_PASSWORD
        self._host = MySQLConfig.MYSQL_HOST
        self._port = MySQLConfig.MYSQL_PORT
        self._DB_NAME = 'provider'

    def _create_database(self, cursor):
        """
        Creates the specified database if it doesn't already exist.

        Args:
            cursor: MySQL cursor object for executing queries.
        """
        try:
            cursor.execute(
                f'CREATE DATABASE {self._DB_NAME} DEFAULT CHARACTER SET "utf8"')
        except mysql.connector.Error as err:
            print(f'Failed creating database: {err}', file=sys.stderr)
            exit(1)

    def create(self):
        """
        Creates the database and tables specified in the _TABLES dictionary.
        """
        self._TABLES = {
            'customers': (
                "CREATE TABLE `customers` ("
                "   `customer_UID` varchar(36) NOT NULL,"
                "   `api_key` varchar(36) NOT NULL,"
                "   PRIMARY KEY (`customer_UID`)"
                ") ENGINE=InnoDB"
            ),
            'meters': (
                "CREATE TABLE `meters`("
                "   `meter_UID` varchar(36) NOT NULL,"
                "   PRIMARY KEY (`meter_UID`)"
                ") ENGINE=InnoDB"
            ),
            'customers_meters': (
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
                ") ENGINE=InnoDB"
            ),
            'users': (
                "CREATE TABLE `users`("
                "   `username` varchar(32) NOT NULL,"
                "   `api_key` varchar(36) NOT NULL,"
                "   PRIMARY KEY (`username`)"
                ") ENGINE=InnoDB"
            )
        }

        # Create connector and cursor
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor()

        # Try to select the database
        try:
            cursor.execute(f'USE {self._DB_NAME}')
        except mysql.connector.Error as err:
            print(f'Database {self._DB_NAME} does not exist.', file=sys.stderr)

            # Call create function if the database does not exist
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self._create_database(cursor=cursor)
                print(f'Database {self._DB_NAME} created successfully', file=sys.stderr)
                cnx.database = self._DB_NAME
            else:
                print(err)
                exit(1)

        # Create all tables
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
        """
        Inserts test data into the 'customers' table.
        """
        # Create connector and cursor
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor()
        cnx.database = self._DB_NAME

        # Test data
        customer_UID_1 = '123456'
        customer_api_key_1 = 'abcdefg'
        customer_UID_2 = '654321'
        customer_api_key_2 = 'gfedcba'

        # SQL statements for inserting test data
        add_customer_1 = "INSERT INTO customers (customer_UID, api_key) VALUES (%s, %s)"
        add_customer_2 = "INSERT INTO customers (customer_UID, api_key) VALUES (%s, %s)"

        # Execute SQL statements
        cursor.execute(add_customer_1, (customer_UID_1, customer_api_key_1))
        cursor.execute(add_customer_2, (customer_UID_2, customer_api_key_2))

        # Commit the changes
        cnx.commit()

        cursor.close()
        cnx.close()

    def get_api_key(self, username: str):
        """
        Retrieves the API key for a given customer UID.

        Args:
            username (str): The username of the admin user.

        Returns:
            str: The API key for the corresponding customer UID, or None if not found.
        """
        # Create connector and cursor
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor(buffered=True)
        cnx.database = self._DB_NAME

        # Query database
        query = ("SELECT api_key FROM users WHERE username=%s")
        cursor.execute(query, (username,))
        api_key = cursor.fetchone()[0] if cursor.rowcount > 0 else None

        # Cleanup
        cursor.close()
        cnx.close()

        return api_key

    def _insert_meter(self, meter_UID: str):
        """
        Inserts a smartmeter UID into the 'meters' table.

        Args:
            meter_UID (str): The smartmeter UID to be inserted.
        """
        # Create connector and cursor
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor(buffered=True)
        cnx.database = self._DB_NAME

        # Query database
        query = ("INSERT INTO meters (meter_UID) VALUES (%s)")
        cursor.execute(query, (meter_UID,))
        cnx.commit()

        # Cleanup
        cursor.close()
        cnx.close()

    def _insert_customer_meter(self, customer_UID: str, meter_UID: str):
        """
        Inserts a customer UID and smartmeter UID into the 'customers_meters' table.

        Args:
            customer_UID (str): The customer UID.
            meter_UID (str): The smartmeter UID.
        """
        # Create connector and cursor
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor(buffered=True)
        cnx.database = self._DB_NAME

        # Query database
        query = ("INSERT INTO customers_meters (customer_UID, meter_UID) VALUES (%s, %s)")
        cursor.execute(query, (customer_UID, meter_UID))
        cnx.commit()

        # Cleanup
        cursor.close()
        cnx.close()

    def delete_customer_meter(self, meter_UID: str):
        """
        Deletes an entry for smartmeter UID in the 'customers_meters' table.

        Args:
            meter_UID (str): The smartmeter UID to be deleted.
        """
        # Create connector and cursor
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor(buffered=True)
        cnx.database = self._DB_NAME

        # Query database
        query = ("DELETE FROM customers_meters WHERE meter_UID = %s")
        cursor.execute(query, (meter_UID,))
        cnx.commit()

        # Cleanup
        cursor.close()
        cnx.close()

    def delete_meter(self, meter_UID: str):
        """
        Deletes an entry for smartmeter UID in the 'meters' table.

        Args:
            meter_UID (str): The smartmeter UID to be deleted.
        """
        # Create connector and cursor
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor(buffered=True)
        cnx.database = self._DB_NAME

        # Query database
        query = ("DELETE FROM meters WHERE meter_UID = %s")
        cursor.execute(query, (meter_UID,))

        # Check the affected row count
        affected_rows = cursor.rowcount

        # Commit the changes
        cnx.commit()

        # Cleanup
        cursor.close()
        cnx.close()

        # Raise an error if no rows were affected
        if affected_rows == 0:
            raise ValueError(f"No meter found with meter_UID: {meter_UID}.")

    def insert_customer(self, customer_UID: str, api_key: str):
        """
        Inserts a customer portal into the 'customers' table.

        Args:
            customer_UID (str): The customer UID.
            api_key (str): The API key for the customer.
        """
        # Create connector and cursor
        cnx = mysql.connector.connect(user=self._user, password=self._password, host=self._host, port=self._port)
        cursor = cnx.cursor(buffered=True)
        cnx.database = self._DB_NAME

        # Query database
        query = ("INSERT INTO customers (customer_UID, api_key) VALUES (%s, %s)")
        cursor.execute(query, (customer_UID, api_key))

        # Commit the changes
        cnx.commit()

        # Cleanup
        cursor.close()
        cnx.close()