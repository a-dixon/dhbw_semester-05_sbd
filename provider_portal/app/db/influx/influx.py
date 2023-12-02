import logging
from datetime import datetime, timezone, timedelta
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from config import config
import sys


logger = logging.getLogger("main")


class InfluxDB:
    """
    A class for interacting with InfluxDB to read and write time-series data.
    """

    def __init__(self):
        """
        Initializes the InfluxDB client and ensures that the specified bucket exists.
        """
        self._token = config.InfluxConfig.INFLUX_TOKEN
        self._bucket = config.InfluxConfig.INFLUX_BUCKET
        self._provider = config.InfluxConfig.INFLUX_PROVIDER
        self._url = config.InfluxConfig.INFLUX_URL
        self._client = InfluxDBClient(url=self._url, token=self._token, org=self._provider, ssl=True, verify_ssl=False)

        bucket_api = self._client.buckets_api()
        if not bucket_api.find_bucket_by_name(self._bucket):
            # Create the bucket if it doesn't exist
            bucket_api.create_bucket(bucket_name=self._bucket, org=self._provider)

    def read(self, start_time, end_time, interval, uid, measurement):
        """
        Reads time-series data from InfluxDB based on the specified parameters.

        Args:
            start_time (str): Start time for the smartmeter data values.
            end_time (str): End time for the smartmeter data values.
            interval (str): Time interval for aggregation.
            uid (str): UID for selecting smartmeter.
            measurement (str): Measurement name for the query.

        Returns:
            list: List of dictionaries containing time and value pairs.
        """
        query = f'''
            from(bucket: "{self._bucket}")
            |> range(start: {start_time}, stop: {end_time})
            |> filter(fn: (r) => r["_measurement"] == "{measurement}" and r["uid"] == "{uid}")
            |> aggregateWindow(every: {interval}, fn: mean)
            |> fill(column: "_value", usePrevious: true)
        '''
        query_api = self._client.query_api()
        tables = query_api.query(org=self._provider, query=query)

        data = []

        for table in tables:
            for record in table.records:
                data.append({
                    "time": record.get_time().isoformat(),
                    "value": record.get_value(),
                })

        return data

    def write(self, timestamp, value, uid, measurement):
        """
        Writes a data point to InfluxDB.

        Args:
            timestamp (str): Timestamp of the data point.
            value (float): Value of the data point.
            uid (str): UID associated with the data point.
            measurement (str): Measurement name for the data point.

        Returns:
            bool: True if the write is successful, False otherwise.
        """
        point = {
            "measurement": measurement,
            "tags": {
                "uid": uid
            },
            "time": timestamp,
            "fields": {
                "float_value": value
            },
        }
        try:
            # Use SYNCHRONOUS write for simplicity and error handling
            write_api = self._client.write_api(write_options=SYNCHRONOUS)
            write_api.write(self._bucket, self._provider, point)
            return True
        except Exception as err:
            logger.error(f"Error writing data to influxdb: {err}")
            return False

    def delete(self, uid):
        """
        Deletes data points associated with a specific UID within the last hour.
        This function is not currently used, as the Buckit used automatically removes
        data that is older than the statutory retention period of 10 years in accordance
        with Section 257 HGB, Art. 6 para. 1 lit. c.

        Args:
            uid (str): UID for filtering data.

        Returns:
            bool: True if the delete is successful, False otherwise.
        """
        try:
            delete_api = self._client.delete_api()

            # Get the current time
            current_time = datetime.now()
            new_time = current_time + timedelta(minutes=60)
            rfc3339_format = '%Y-%m-%dT%H:%M:%SZ'
            new_time_rfc3339 = new_time.strftime(rfc3339_format)

            # Executing delete request
            delete_api.delete("1970-01-01T00:00:00Z", new_time_rfc3339, '_measurement="consumption"', f'uid="{uid}"', org=self._provider, bucket=self._bucket)

            return True
        except Exception as err:
            logger.error(f"Error deleting data from influxdb: {err}")
            return False