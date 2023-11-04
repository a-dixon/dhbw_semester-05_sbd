import random
import time
from datetime import datetime
from smart_meter.api.api import APIHandler


class SmartMeter:
    def __init__(self, uid):
        self._consumption = []
        self._uid = uid
        self._api = APIHandler("test.com", uid)

    @staticmethod
    def _generate_consumption(current_time):
        consumption = 1
        random_factor = random.uniform(-0.1, 0.1)
        randomized_consumption = consumption + (consumption * random_factor)
        return randomized_consumption

    def _write_consumption(self):
        current_time = datetime.now()

        if self._consumption:
            last_time, _ = self._consumption[len(self._consumption) - 1]
            difference = (current_time - last_time).total_seconds()
            if difference >= 1:
                consumption = self._generate_consumption(current_time)
                self._consumption.append((current_time, consumption))
        else:
            consumption = self._generate_consumption(current_time)
            self._consumption.append((current_time, consumption))

    def _delete(self, timestamp):
        self._consumption = [(t, v) for t, v in self._consumption if t > timestamp]

    def _transfer(self):
        data_list = []
        for i in range(0, 60):
            timestamp, value = self._consumption[i]
            rounded_timestamp = timestamp.isoformat()
            data_point = {
                "timestamp": rounded_timestamp,
                "value": value
            }
            data_list.append(data_point)
        json_data = {
            "data": data_list
        }
        print(json_data)
        # status = self.api.send_data(json_data)
        status = True
        last_timestamp, _ = self._consumption[59]
        if status:
            self._delete(last_timestamp)

    def run_smart_meter(self):
        while True:
            self._write_consumption()
            if len(self._consumption) > 60:
                self._transfer()
            time.sleep(0.2)  # Möglichkeit finden dieses Zeit dynamisch zu ändern
