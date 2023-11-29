import sys
import cryptography
from cryptography import x509
from cryptography.hazmat._oid import NameOID
from app.db.influx.influx import InfluxDB


class SmartmeterAPI:
    """
    A class for handling authentication and adding measurements to InfluxDB for smart meters
    """

    def __init__(self, raw_cert, uid):
        """
        Initializes the SmartmeterAPI with the raw certificate and UID.

        Args:
            raw_cert (str): The raw certificate string.
            uid (str): The UID associated with the Smart Meter.
        """
        self._uid = uid
        self._raw_cert = raw_cert

    @staticmethod
    def _get_common_name(cert):
        """
        Helper method to extract the Common Name (CN) from the certificate.

        Args:
            cert: The x509 certificate.

        Returns:
            str: The Common Name (CN) from the certificate.
        """
        return cert[0].subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

    def authenticate_smartmeter(self):
        """
        Authenticates the Smart Meter based on the UID and the Common Name (CN) in the certificate.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        try:
            # Load the PEM certificate
            client_cert = cryptography.x509.load_pem_x509_certificates(self._raw_cert.encode("utf-8"))
            common_name = self._get_common_name(client_cert)

            # Check if the Common Name (CN) matches the UID
            if common_name == self._uid:
                return True
            else:
                return False
        except:
            # Return False if any exception occurs during authentication
            return False

    def add_measurements(self, datapoints):
        """
        Adds measurements to InfluxDB for the Smart Meter.

        Args:
            datapoints (list): List of datapoints containing timestamp and value.

        Returns:
            bool: True if all measurements are added successfully, False if any fails.
        """
        successful = True
        influxdb = InfluxDB()

        for datapoint in datapoints:
            timestamp = datapoint["timestamp"]
            value = datapoint["value"]
            uid = self._uid
            measurement = "consumption"

            # Try to write the measurement to InfluxDB, set successful to False if any write fails
            if not influxdb.write(timestamp, value, uid, measurement):
                successful = False

        return successful