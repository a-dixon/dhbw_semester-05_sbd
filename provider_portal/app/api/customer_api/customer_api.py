import logging
import sys
import shutil
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from config import config
from app.db.mysql.mysql import MySQL
from app.db.influx.influx import InfluxDB
from app.utils.certificates.gen_client_certificates import generate_client_certificate


logger = logging.getLogger("main")


class CustomerAPI:
    """
    Customer API class for managing interactions providers.
    """

    def __init__(self, customer_UID: str, api_key: str):
        """
        Initialize the CustomerAPI instance.

        Parameters:
            - customer_UID (str): Unique identifier for the customer.
            - api_key (str): API key for authenticating the customer.
        """
        self._customer_UID = customer_UID
        self._api_key = api_key

    @staticmethod
    def _generate_meter_UID():
        """
        Generate a unique meter ID using the uuid4 function.

        Returns:
            str: Unique meter ID.
        """
        return str(uuid4())

    def authenticate_customer_portal(self):
        """
        Authenticate the customer portal based on the provided API key.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """

        # --- Get expected API key from database ---
        mysql = MySQL()

        try:
            expected_api_key = mysql.get_api_key_from_customer(self._customer_UID)
        except:
            return False

        # --- Return if API keys are equal ---
        return expected_api_key == self._api_key

    def create_meter(self):
        """
        Create a new smart meter, generating a unique meter UID and associating it with the customer.

        Returns:
            str: The newly generated meter UID.
        """
        # --- Generate new meter UID ---
        meter_UID = self._generate_meter_UID()

        mysql = MySQL()

        try:
            mysql.insert_meter(meter_UID=meter_UID)

        except Exception as err:
            logger.error(f"Smart meter could not be inserted into meters database: {err}")
            raise err

        try:
            mysql.insert_customer_meter(customer_UID=self._customer_UID, meter_UID=meter_UID)

        except Exception as err:
            logger.error(f"Smart meter could not be inserted into customer_meters database: {err}")
            raise err

        generate_client_certificate(meter_UID)

        return meter_UID

    def get_meter_measurements(self, start_time, end_time, data_interval, meter_UID):
        """
        Get smart meter measurements within a specified time range.

        Parameters:
            - start_time (str): The start time for the measurements.
            - end_time (str): The end time for the measurements.
            - data_interval (str): The time interval between data points.
            - meter_UID (str): The unique identifier of the smart meter.

        Returns:
            list: List of dictionaries containing timestamp and corresponding values.
        Raises:
            ValueError: If the specified time range is in the future or exceeds the maximum data points allowed.
        """
        # Check if end_time is in the future
        current_time = datetime.now(timezone(timedelta(hours=1)))
        if datetime.fromisoformat(end_time.replace(" ", "+")) > current_time:
            raise ValueError("error_no_data")

        # Check the number of data points based on the specified time range and data interval
        time_diff = datetime.fromisoformat(end_time.replace(" ", "+")) - datetime.fromisoformat(
            start_time.replace(" ", "+"))
        num_data_points = int(time_diff.total_seconds() / int(data_interval))

        if num_data_points > 3600:
            raise ValueError("error_over_maximum")

        converted_start_time = start_time.replace(" ", "+")
        converted_end_time = end_time.replace(" ", "+")
        converted_data_interval = data_interval + "s"

        influxdb = InfluxDB()
        reading = influxdb.read(start_time=converted_start_time, end_time=converted_end_time,
                                interval=converted_data_interval, uid=meter_UID, measurement="consumption")

        return reading

    def delete_meter(self, meter_UID):
        """
        Delete a smart meter, including its association with the customer and certificate.

        Parameters:
            - meter_UID (str): The unique identifier of the smart meter.
        Raises:
            Exception: If deletion from the database or file system fails.
        """
        mysql = MySQL()

        try:
            mysql.delete_customer_meter(meter_UID=meter_UID)

        except Exception as err:
            logger.error(f"Smart meter could not be deleted from customer_meters database: {err}")
            raise err

        try:
            mysql.delete_meter(meter_UID=meter_UID)
            # influxdb.delete(meter_UID)
        except Exception as err:
            logger.error(f"Smart meter could not be deleted from meters database: {err}")
            raise err

        try:
            path = f"{config.CertificateConfig.CLIENT_CERT_DIRECTORY}/{meter_UID}"
            shutil.rmtree(path)

        except Exception as err:
            logger.error(f"Smart meter could not be deleted from smartmeter wrapper: {err}")
            raise err