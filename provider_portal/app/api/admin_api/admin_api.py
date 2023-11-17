import sys
from uuid import uuid4
from app.db.mysql.mysql import MySQL


class AdminAPI:
    ''' Admin API class'''

    def __init__(self, api_key: str, username: str):
        self._username = username
        self._api_key = api_key


    @staticmethod
    def _generate_UID():
        ''' Generate unique ID based on uuid4 function'''
        return str(uuid4())
    

    def authenticate_admin_user(self):
        ''' Assert api_key and username'''
        # --- Get expected API key from database ---
        mysql = MySQL()
        expected_api_key = mysql.get_user_api_key(self._username)

        # --- Return if API keys are equal ---
        return expected_api_key == self._api_key
    

    def create_customer_portal(self):
        ''' Create new customer portal'''
        # --- Generate customer_uid and api_key
        customer_UID = self._generate_UID()
        api_key = self._generate_UID()

        mysql = MySQL()

        try:
            mysql._insert_customer(customer_UID=customer_UID)

        except Exception as err:
            print('Customer portal could not be inserted into database.', file=sys.stderr)
            print(err, file=sys.stderr)
            raise err
        
        return customer_UID, api_key
