from uuid import uuid4
from app.db.mysql.mysql import MySQL
from app.db.influx.influx import InfluxDB


class CustomerAPI():
    ''' Customer API class'''

    def __init__(self, customer_UID: str, api_key: str):
        self._customer_UID = customer_UID

        if not self._authenticate_customer_portal(api_key):
            return False
   

    @staticmethod
    def _generate_meter_UID(self):
        ''' Generate unique meter ID based on uuid4 function'''
        return str(uuid4())
    

    def _authenticate_customer_portal(self, api_key: str):
        ''' Assert passed api_key is equal to api_key in db.'''
        # --- Get expected API key from database ---
        mysql = MySQL()
        expected_api_key = mysql.get_api_key(self._customer_UID)

        # --- Return if API keys are equal ---
        return expected_api_key == api_key

    
    def create_meter(self):
        ''' Create new smart meter.'''
        self._meter_UID = self._generate_meter_UID()

        # TODO:
        # database entry in meters with meter_UID
        # database entry in customers-meters with customer_UID and meter_UID
        # pass UID to Joshuas script

        return self._meter_UID


    def get_meter_measurements(self, start_time, end_time, data_interval, meter_uid):
        ''' Get smart meter measurements.'''
        # TODO:
        # get measurements in defined range from InfluxDB
        influxdb = InfluxDB()
        reading = influxdb.read(start_time=start_time, end_time=end_time, interval=data_interval, uid=meter_uid)
        # print(influxdb.read(start_time="2023-11-05T21:34:00.000Z", end_time="2023-11-05T21:35:00.000Z", interval="1s",uid="040506", measurement="consumption"), file=sys.stderr)

        pass


    def delete_meter(self):
        ''' Delete smart meter.'''
        # TODO:
        # delete database entry in meters with meter_UID
        # delete database entry in customers-meters with customer_UID and meter_UID 
        pass
