from uuid import uuid4


class CustomerAPI():
    ''' Customer API class'''

    def __init__(self, customer_UID: str, api_key: str):
        self._customer_UID = customer_UID

        if not self._authenticate_customer_portal(api_key):
            return False   


    def _authenticate_customer_portal(self, apiKey: str):
        # TODO:
        # check if api key exists in database in combination with customer UID
        pass


    def _generate_meter_UID(self):
        ''' Generate unique meter ID based on uuid4 function'''
        return str(uuid4())

    
    def create_meter(self):
        ''' Create new smart meter.'''
        self._meter_UID = self._generate_meter_UID()

        # TODO:
        # database entry in meters with meter_UID
        # database entry in customers-meters with customer_UID and meter_UID 
        return self._meter_UID


    def get_meter_measurements(self):
        ''' Get smart meter measurements.'''
        # TODO:
        # get measurements in defined range from InfluxDB
        pass


    def delete_meter(self):
        ''' Delete smart meter.'''
        # TODO:
        # delete database entry in meters with meter_UID
        # delete database entry in customers-meters with customer_UID and meter_UID 
        pass
