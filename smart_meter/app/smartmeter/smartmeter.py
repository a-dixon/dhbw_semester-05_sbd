import random
import time
from datetime import datetime
from app.api.api import APIHandler
from config import config


class SmartMeter:
    def __init__(self, uid):
        self._consumption = []
        self._uid = uid
        self._api = APIHandler(config.API_URL, uid)

    @staticmethod
    def _generate_consumption(current_time):
        consumption = 1
        random_factor = random.uniform(-0.1, 0.1)
        randomized_consumption = consumption + (consumption * random_factor)
        return randomized_consumption

    def _write_consumption(self, time_between_datapoints):
        current_time = datetime.now()

        if self._consumption:
            last_time, _ = self._consumption[len(self._consumption) - 1]
            difference = (current_time - last_time).total_seconds()
            if difference >= time_between_datapoints:
                consumption = self._generate_consumption(current_time)
                self._consumption.append((current_time, consumption))
        else:
            consumption = self._generate_consumption(current_time)
            self._consumption.append((current_time, consumption))

    def _delete(self, timestamp):
        self._consumption = [(t, v) for t, v in self._consumption if t > timestamp]

    def _transfer(self, datapoints_until_send):
        data_list = []
        for i in range(0, datapoints_until_send):
            timestamp, value = self._consumption[i]
            rounded_timestamp = timestamp.isoformat()
            data_point = {
                "timestamp": rounded_timestamp,
                "value": value
            }
            data_list.append(data_point)

        status = self._api.send_data(data_list)
        last_timestamp, _ = self._consumption[datapoints_until_send-1]
        if status:
            self._delete(last_timestamp)

    def run_smart_meter(self, datapoints_unitl_send, time_between_datapoints):
        while True:
            self._write_consumption(time_between_datapoints)
            if len(self._consumption) > datapoints_unitl_send:
                self._transfer(datapoints_unitl_send)
            time.sleep(0.2)
