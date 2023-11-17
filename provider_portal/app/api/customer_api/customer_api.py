import sys
import shutil
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from config import config
from app.db.mysql.mysql import MySQL
from app.db.influx.influx import InfluxDB
from app.utils.certificates.gen_client_certificates import generate_client_certificate


class CustomerAPI:
    ''' Customer API class'''

    def __init__(self, customer_UID: str, api_key: str):
        self._customer_UID = customer_UID
        self._api_key = api_key
   

    @staticmethod
    def _generate_meter_UID():
        ''' Generate unique meter ID based on uuid4 function'''
        return str(uuid4())
    

    def authenticate_customer_portal(self):
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

        return meter_UID


    def get_meter_measurements(self, start_time, end_time, data_interval, meter_UID):
        ''' Get smart meter measurements.'''

        # Check if end_time is in the future
        current_time = datetime.now(timezone(timedelta(hours=1)))
        if datetime.fromisoformat(end_time.replace(" ", "+")) > current_time:
            raise ValueError("error_no_data")

        # Check the number of data points based on the specified time range and data interval
        time_diff = datetime.fromisoformat(end_time.replace(" ", "+")) - datetime.fromisoformat(
            start_time.replace(" ", "+"))
        num_data_points = int(time_diff.total_seconds() / int(data_interval))

        if num_data_points > 3600:
            raise ValueError("error_over_maximum")

        print(start_time.replace(" ", "+"), file=sys.stderr)
        converted_start_time = start_time.replace(" ", "+")
        converted_end_time = end_time.replace(" ", "+")
        converted_data_interval = data_interval + "s"

        influxdb = InfluxDB()
        reading = influxdb.read(start_time=converted_start_time, end_time=converted_end_time, interval=converted_data_interval, uid=meter_UID, measurement="consumption")

        return reading


    def delete_meter(self, meter_UID):
        ''' Delete smart meter.'''
        
        mysql = MySQL()
        influxdb = InfluxDB()

        try:
            mysql.delete_customer_meter(meter_UID=meter_UID)
        except Exception as err:
            print('Smart meter could not be deleted from customer_meters database.', file=sys.stderr)
            print(err, file=sys.stderr)
            raise err
        
        try:
            mysql.delete_meter(meter_UID=meter_UID)
            # influxdb.delete(meter_UID)
        except Exception as err:
            print('Smart meter could not be deleted from meters database.', file=sys.stderr)
            print(err, file=sys.stderr)
            raise err

        try:
            path = f"{config.CLIENT_CERT_DIRECTORY}/{meter_UID}"
            shutil.rmtree(path)
        except Exception as err:
            print('Smart meter could not be deleted from smartmeter wrapper.', file=sys.stderr)
            print(err, file=sys.stderr)
            raise err
