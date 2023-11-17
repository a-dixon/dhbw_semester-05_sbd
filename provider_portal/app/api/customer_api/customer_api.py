import sys
from uuid import uuid4
from app.db.mysql.mysql import MySQL
from app.db.influx.influx import InfluxDB
from app.utils.certificates.gen_client_certificates import generate_client_certificate


class CustomerAPI:
    ''' Customer API class'''

    def __init__(self, customer_UID: str, api_key: str):
        self._customer_UID = customer_UID
        self._api_key = api_key

        if not self._authenticate_customer_portal():
            return False
   

    @staticmethod
    def _generate_meter_UID(self):
        ''' Generate unique meter ID based on uuid4 function'''
        return str(uuid4())
    

    def _authenticate_customer_portal(self):
        ''' Assert passed api_key is equal to api_key in db.'''
        # --- Get expected API key from database ---
        mysql = MySQL()
        expected_api_key = mysql.get_api_key(self._customer_UID)

        # --- Return if API keys are equal ---
        return expected_api_key == self._api_key

    
    def create_meter(self):
        ''' Create new smart meter.'''
        # --- Generate new meter UID ---
        meter_UID = self._generate_meter_UID()

        # --- Insert into DB ---
        mysql = MySQL()

        try:
            mysql._insert_meter(meter_UID=meter_UID)
        except Exception as err:
            print('Smart meter could not be inserted into meters database.', file=sys.stderr)
            print(err, file=sys.stderr)
            raise err
        try:
            mysql._insert_customer_meter(customer_UID=self._customer_UID, meter_UID=meter_UID)
        except Exception as err:
            print('Smart meter could not be inserted into customer_meters database.', file=sys.stderr)
            print(err, file=sys.stderr)
            raise err

        generate_client_certificate(meter_UID)
        # TODO:
        # pass UID to Joshuas script

        return self._meter_UID


    def get_meter_measurements(self, start_time, end_time, data_interval, meter_UID):
        ''' Get smart meter measurements.'''
        # TODO:
        # get measurements in defined range from InfluxDB
        influxdb = InfluxDB()
        reading = influxdb.read(start_time=start_time, end_time=end_time, interval=data_interval, uid=meter_UID)
        # print(influxdb.read(start_time="2023-11-05T21:34:00.000Z", end_time="2023-11-05T21:35:00.000Z", interval="1s",uid="040506", measurement="consumption"), file=sys.stderr)

        pass


    def delete_meter(self, meter_UID):
        ''' Delete smart meter.'''
        
        mysql = MySQL()

        try:
            mysql._delete_customer_meter(customer_UID=self._customer_UID, meter_UID=meter_UID)
        except Exception as err:
            print('Smart meter could not be deleted from customer_meters database.', file=sys.stderr)
            print(err, file=sys.stderr)
            raise err
        
        try:
            mysql.delete_meter(meter_UID=meter_UID)
        except Exception as err:
            print('Smart meter could not be deleted from meters database.', file=sys.stderr)
            print(err, file=sys.stderr)
            raise err
