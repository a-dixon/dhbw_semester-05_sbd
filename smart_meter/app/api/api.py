import requests
import json
from config import config


class APIHandler:
    def __init__(self, api_url, uid):
        """
        Initialize the APIHandler instance.

        Parameters:
        - api_url (str): The URL of the API endpoint.
        - uid (str): The unique identifier associated with the meter.
        """
        self._api_url = api_url
        self._uid = uid

    def send_data(self, data):
        """
        Send data to the specified API endpoint.

        Parameters:
        - data (dict): The data to be sent.

        Returns:
        - bool: True if the data was successfully sent, False otherwise.
        """
        headers = {
            'Content-Type': 'application/json'
        }

        # Paths to client certificates
        certificates = (f"{config.CertificateConfig.CERT_DIRECTORY}/{self._uid}/client-public-key.pem",
                        f"{config.CertificateConfig.CERT_DIRECTORY}/{self._uid}/client-private-key.pem")

        post_data = {
            "meterUID": self._uid,
            "data": data
        }

        if not certificates:
            # If certificates are not available, return False
            return False

        try:
            # Send a POST request to the API endpoint
            response = requests.post(self._api_url, data=json.dumps(post_data),
                                     headers=headers, cert=certificates, verify=config.CertificateConfig.ROOT_CA_PEM)

            if response.status_code == 200:
                # If the response status code is 200, consider it a success
                return True
            else:
                # Otherwise, consider it a failure
                return False
        except Exception as e:
            # Handle exceptions and return False
            print(e)
            return False