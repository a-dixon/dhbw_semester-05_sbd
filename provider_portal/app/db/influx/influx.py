from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDB:
    def __init__(self):
        self._token = "DzFwd-VxKfwt4Y20okuIDbolk3X8bcsGLOMDM0mp2IsdImr-Uji5JrclSyHmuUo-QLgIUmyQYJXzRhqKjNmmXQ=="
        self._bucket = "smartmeter"
        self._provider = "provider"
        self._url = "http://10.0.1.30:8086"
        self._client = InfluxDBClient(url=self._url, token=self._token, org=self._provider)

        bucket_api = self._client.buckets_api()
        if not bucket_api.find_bucket_by_name(self._bucket):
            bucket_api.create_bucket(bucket_name=self._bucket, org=self._provider)

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
        write_api = self._client.write_api(write_options=SYNCHRONOUS)
        write_api.write(self._bucket, self._provider, point)
