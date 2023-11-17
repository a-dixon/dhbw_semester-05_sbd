import sys

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from config import config


class InfluxDB:
    def __init__(self):
        self._token = config.INFLUX_TOKEN
        self._bucket = config.INFLUX_BUCKET
        self._provider = config.INFLUX_PROVIDER
        self._url = config.INFLUX_URL
        self._client = InfluxDBClient(url=self._url, token=self._token, org=self._provider)

        bucket_api = self._client.buckets_api()
        if not bucket_api.find_bucket_by_name(self._bucket):
            bucket_api.create_bucket(bucket_name=self._bucket, org=self._provider)

    def read(self, start_time, end_time, interval, uid, measurement):
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
                    "time": record.get_time(),
                    "value": record.get_value(),
                })

        return data

    def write(self, timestamp, value, uid, measurement):
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
            write_api = self._client.write_api(write_options=SYNCHRONOUS)
            write_api.write(self._bucket, self._provider, point)
            return True
        except:
            return False

    def delete(self, uid):
        query = f'''
                    from(bucket: "{self._bucket}")
                    |> range(start: 0)
                    |> filter(fn: (r) => r["uid"] == "{uid}")
                    |> delete()
                '''
        try:
            query_api = self._client.query_api()
            query_api.query(org=self._provider, query=query)
            return True
        except Exception:
            return False