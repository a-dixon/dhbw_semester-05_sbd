import requests
import json
from config import config

class APIHandler:
    def __init__(self, api_url, uid):
        self._api_url = api_url
        self._uid = uid

    def send_data(self, data):
        headers = {
            'Content-Type': 'application/json'
        }

        # certificates = (f"{config.CERT_DIRECTORY}/{self._uid}/client.crt", f"{config.CERT_DIRECTORY}/{self._uid}/client.key")
        certificates = (f"{config.CertificateConfig.CERT_DIRECTORY}/{self._uid}/client-public-key.pem", f"{config.CertificateConfig.CERT_DIRECTORY}/{self._uid}/client-private-key.pem")

        post_data = {
            "meterUID": self._uid,
            "data": data
        }

        if not certificates:
            return False
        try:
            response = requests.post(self._api_url, data=json.dumps(post_data), headers=headers, cert=certificates, verify=config.CertificateConfig.ROOT_CA_PEM)
            # response = requests.post(self._api_url, data=json.dumps(post_data), headers=headers, cert=certificates, verify=False)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
