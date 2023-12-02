import time
import unittest
from datetime import datetime, timedelta

import requests


class TestCustomerAPI(unittest.TestCase):
    meter_uid = None

    def setUp(self):
        self.api_key = "247b9f5a-600f-4b46-a8a3-912657dd1425"
        self.customer_uid = "ef809ffa-8872-4354-806b-f7fede0e4d75"
        self.api_url_create = "https://10.0.1.10/v1/provider/meter-create"
        self.api_url_measurements = f"https://10.0.1.10/v1/provider/meter-measurements"
        self.api_url_delete = "https://10.0.1.10/v1/provider/meter-delete"

    def test_meter_creation_success(self):
        headers = {"Authorization": f"{self.api_key}", "Content-Type": "application/json"}
        data = {"customerUID": self.customer_uid}

        response = requests.post(self.api_url_create, json=data, headers=headers, verify=False)
        result = response.json()

        TestCustomerAPI.meter_uid = result["meterUID"]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["message"], "Smart Meter wurde erfolgreich angelegt.")

        time.sleep(65)

    def test_meter_creation_invalid_key(self):
        headers = {"Authorization": f"22222", "Content-Type": "application/json"}
        data = {"customerUID": self.customer_uid}

        response = requests.post(self.api_url_create, json=data, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Customer Portal konnte nicht authentifiziert werden.")

    def test_meter_creation_invalid_customer_uid(self):
        headers = {"Authorization": f"{self.api_key}", "Content-Type": "application/json"}
        data = {"customerUID": "test1243"}

        response = requests.post(self.api_url_create, json=data, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Customer Portal konnte nicht authentifiziert werden.")

    def test_meter_creation_invalid_format(self):
        headers = {"Authorization": f"{self.api_key}", "Content-Type": "application/json"}
        data = {"customerUI": "test1243"}

        response = requests.post(self.api_url_create, json=data, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Das Format konnte nicht dekodiert werden.")

    def test_meter_measurements_success(self):
        headers = {"Authorization": f"{self.api_key}"}

        start_time = (datetime.utcnow() - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

        params = {
            "customerUID": self.customer_uid,
            "meterUID": TestCustomerAPI.meter_uid,
            "startTime": start_time,
            "endTime": end_time,
            "dataInterval": 1
        }

        response = requests.get(self.api_url_measurements, params=params, headers=headers, verify=False)
        result = response.json()

        data = result["data"]
        for datapoint in data:
            self.assertTrue(datapoint["time"] is not None)
            self.assertTrue(datapoint["value"] is not None)

        self.assertEqual(response.status_code, 200)

    def test_meter_measurements_invalid_key(self):
        headers = {"Authorization": f"key"}

        start_time = (datetime.utcnow() - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

        params = {
            "customerUID": self.customer_uid,
            "meterUID": TestCustomerAPI.meter_uid,
            "startTime": start_time,
            "endTime": end_time,
            "dataInterval": 1
        }

        response = requests.get(self.api_url_measurements, params=params, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Customer Portal konnte nicht authentifiziert werden.")

    def test_meter_measurements_invalid_format(self):
        headers = {"Authorization": f"{self.api_key}"}

        start_time = (datetime.utcnow() - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

        params = {
            "customerUID": self.customer_uid,
            "meterUID": TestCustomerAPI.meter_uid,
            "starTime": start_time,
            "endTime": end_time,
            "dataInterval": 1
        }

        response = requests.get(self.api_url_measurements, params=params, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Das Format konnte nicht dekodiert werden.")

    def test_meter_measurements_invalid_customer_uid(self):
        headers = {"Authorization": f"{self.api_key}"}

        start_time = (datetime.utcnow() - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

        params = {
            "customerUID": "test123",
            "meterUID": TestCustomerAPI.meter_uid,
            "startTime": start_time,
            "endTime": end_time,
            "dataInterval": 1
        }

        response = requests.get(self.api_url_measurements, params=params, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Customer Portal konnte nicht authentifiziert werden.")

    def test_meter_measurements_max_points(self):
        headers = {"Authorization": f"{self.api_key}"}

        start_time = (datetime.utcnow() - timedelta(minutes=120)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

        params = {
            "customerUID": self.customer_uid,
            "meterUID": TestCustomerAPI.meter_uid,
            "startTime": start_time,
            "endTime": end_time,
            "dataInterval": 1
        }

        response = requests.get(self.api_url_measurements, params=params, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"],
                         "Die Anzahl der angeforderten Messpunkte überschreitet das Maximum. Bitte reduzieren Sie das Abfrageintervall oder teilen Sie die Anfrage auf.")

    def test_meter_measurements_max_points(self):
        headers = {"Authorization": f"{self.api_key}"}

        start_time = (datetime.utcnow() - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        end_time = (datetime.utcnow() + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S+00:00")

        params = {
            "customerUID": self.customer_uid,
            "meterUID": TestCustomerAPI.meter_uid,
            "startTime": start_time,
            "endTime": end_time,
            "dataInterval": 1
        }

        response = requests.get(self.api_url_measurements, params=params, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["message"], "Keine Daten im angegebenen Zeitraum vorhanden.")

    def test_meter_deletion_success(self):
        headers = {"Authorization": f"{self.api_key}", "Content-Type": "application/json"}
        data = {"meterUID": TestCustomerAPI.meter_uid, "customerUID": self.customer_uid}

        response = requests.delete(self.api_url_delete, json=data, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["message"], "Smart Meter wurde erfolgreich gelöscht.")

    def test_meter_deletion_invalid_key(self):
        headers = {"Authorization": f"test", "Content-Type": "application/json"}
        data = {"meterUID": TestCustomerAPI.meter_uid, "customerUID": self.customer_uid}

        response = requests.delete(self.api_url_delete, json=data, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Customer Portal konnte nicht authentifiziert werden.")

    def test_meter_deletion_invalid_customer_uid(self):
        headers = {"Authorization": f"{self.api_key}", "Content-Type": "application/json"}
        data = {"meterUID": TestCustomerAPI.meter_uid, "customerUID": "hans"}

        response = requests.delete(self.api_url_delete, json=data, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Customer Portal konnte nicht authentifiziert werden.")

    def test_meter_deletion_invalid_format(self):
        headers = {"Authorization": f"{self.api_key}", "Content-Type": "application/json"}
        data = {"meterID": TestCustomerAPI.meter_uid, "customerUID": self.customer_uid}

        response = requests.delete(self.api_url_delete, json=data, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Das Format konnte nicht dekodiert werden.")

    def test_meter_deletion_invalid_meter_uid(self):
        headers = {"Authorization": f"{self.api_key}", "Content-Type": "application/json"}
        data = {"meterUID": "1234", "customerUID": self.customer_uid}

        response = requests.delete(self.api_url_delete, json=data, headers=headers, verify=False)
        result = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["message"], "Die Kombination von Meter UID und Customer UID existiert nicht.")


if __name__ == '__main__':
    unittest.main()
