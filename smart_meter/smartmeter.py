import random
import time
from datetime import datetime
from api import APIHandler


class SmartMeter:
    def __init__(self, uid):
        self.consumption = []
        self.uid = uid
        self.api = APIHandler("test.com", uid)

    @staticmethod
    def generate_consumption(current_time):
        consumption = 1
        random_factor = random.uniform(-0.1, 0.1)
        randomized_consumption = consumption + (consumption * random_factor)
        return randomized_consumption

    def write_consumption(self):
        current_time = datetime.now()

        if self.consumption:
            last_time, _ = self.consumption[len(self.consumption) - 1]
            difference = (current_time - last_time).total_seconds()
            if difference >= 1:
                consumption = self.generate_consumption(current_time)
                self.consumption.append((current_time, consumption))
        else:
            consumption = self.generate_consumption(current_time)
            self.consumption.append((current_time, consumption))

    def delete(self, timestamp):
        self.consumption = [(t, v) for t, v in self.consumption if t > timestamp]

    def transfer(self):
        data_list = []
        for i in range(0, 60):
            timestamp, value = self.consumption[i]
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
        last_timestamp, _ = self.consumption[59]
        if status:
            self.delete(last_timestamp)

    def run_smart_meter(self):
        while True:
            self.write_consumption()
            if len(self.consumption) > 60:
                self.transfer()
            time.sleep(0.2)  # Möglichkeit finden dieses Zeit dynamisch zu ändern
