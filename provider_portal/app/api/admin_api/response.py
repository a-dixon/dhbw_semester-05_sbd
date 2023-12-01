import sys
from flask import jsonify


class Response:

    # Define messages and their corresponding HTTP status codes
    MESSAGES = {
        "success_create_customer": ("Customer Portal wurde erfolgreich angelegt.", 201),
        "error_create_customer": ("Customer Portal konnte nicht angelegt werden.", 409),
        "error_decoding": ("Das Format konnte nicht dekodiert werden.", 400),
        "error_authentication": ("Admin User konnte nicht authentifiziert werden.", 400),
        "success_delete_customer": ("Customer Portal wurde erfolgreich gelöscht.", 200),
        "error_delete_customer": ("Customer Portal konnte nicht gelöscht werden.", 404),
        "success_list_customer_portals": ("Customer Portals wurden erfolgreich aufgelistet.", 200),
        "success_list_smart_meters": ("Smart Meters wurden erfolgreich aufgelistet.", 200),
        "error_list_smart_meters": ("Smart Meters konnten nicht aufgelistet werden.", 500),
        "error_list_customer_portals": ("Customer Portals konnten nicht aufgelistet werden.", 500)
    }

    def __init__(self, dict):
        """
        Initializes the Response object with a dictionary.

        Args:
            dict (dict): A dictionary containing response data.
        """
        self._dict = dict

    def select_message(self, message):
        """
        Selects the message and status code based on the provided key.

        Args:
            message (str): The key corresponding to the desired message.

        Returns:
            tuple: A tuple containing the selected message and its HTTP status code.
        """
        return Response.MESSAGES.get(message)

    def create_response(self):
        """
        Creates a Flask JSON response using the provided dictionary.

        Returns:
            flask.Response: A Flask JSON response.
        """
        message, status_code = self.select_message(self._dict["message"])

        if "customer_UID" and "customer_api_key" in self._dict:
            response = jsonify({"message": message, "customer_UID": self._dict["customer_UID"], "customer_api_key": self._dict["customer_api_key"]})
            response.status_code = status_code
            return response
        elif "customer_portals" in self._dict:
            response = jsonify({"message": message, "customer_portals": self._dict["customer_portals"]})
            response.status_code = status_code
            return response
        elif "meters" in self._dict:
            response = jsonify({"message": message, "meters": self._dict["meters"]})
            response.status_code = status_code
            return response
        else:
            response = jsonify({"message": message})
            response.status_code = status_code
            return response
    