import random
import threading
import time
from datetime import datetime
from app.api.api import APIHandler
from config import config


class SmartMeter:
    def __init__(self, uid):
        """
        Initialize the SmartMeter instance.

        Parameters:
        - uid (str): The unique identifier associated with the meter.
        """
        self._consumption = []
        self._uid = uid
        self._api = APIHandler(config.APIConfig.API_URL, uid)

    @staticmethod
    def _generate_consumption(current_time):
        """
        Generate a random consumption value with a slight variation.

        Parameters:
        - current_time (datetime): The current timestamp.

        Returns:
        - float: Randomized consumption value.
        """
        consumption = 1
        random_factor = random.uniform(-0.1, 0.1)
        randomized_consumption = consumption + (consumption * random_factor)
        return randomized_consumption

    def _write_consumption(self, time_between_datapoints):
        """
        Generate and append consumption data if enough time has passed.

        Parameters:
        - time_between_datapoints (int): Time interval between each data point.
        """
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
        """
        Delete consumption data points older than the specified timestamp.

        Parameters:
        - timestamp (datetime): The timestamp used as a reference for deletion.
        """
        self._consumption = [(t, v) for t, v in self._consumption if t > timestamp]

    def _transfer(self, datapoints_until_send):
        """
        Transfer consumption data to the API endpoint.

        Parameters:
        - datapoints_until_send (int): Number of data points to transfer at once.
        """
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
        """
        Run the smart meter simulation.

        Parameters:
        - datapoints_unitl_send (int): Number of data points to accumulate before sending to the API.
        - time_between_datapoints (int): Time interval between each data point generation.
        """
        while getattr(threading.current_thread(), "do_run", True):
            self._write_consumption(time_between_datapoints)
            if len(self._consumption) > datapoints_unitl_send:
                self._transfer(datapoints_unitl_send)
            time.sleep(0.2)

    def get_uid(self):
        """
        Get the unique identifier associated with the smart meter.

        Returns:
        - str: The smart meter's unique identifier.
        """
        return self._uid