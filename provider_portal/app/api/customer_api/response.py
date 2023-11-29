import sys
from flask import jsonify

class Response:
    # Define messages and their corresponding HTTP status codes
    MESSAGES = {
        "success_create_meter": ("Smart Meter wurde erfolgreich angelegt.", 201),
        "success_delete_meter": ("Smart Meter wurde erfolgreich gelöscht.", 200),

        "error_create_meter": ("Smart Meter konnte nicht angelegt werden. Die Kombination von Meter UID und Customer UID existiert bereits.", 409),
        "error_meter_customer_combination": ("Die Kombination von Meter UID und Customer UID existiert nicht.", 404),
        "error_no_data": ("Keine Daten im angegebenen Zeitraum vorhanden.", 404),
        "error_over_maximum": ("Die Anzahl der angeforderten Messpunkte überschreitet das Maximum. Bitte reduzieren Sie das Abfrageintervall oder teilen Sie die Anfrage auf.", 400),
        "error_decoding": ("Das Format konnte nicht dekodiert werden.", 400),

        "error_authentication": ("Customer Portal konnte nicht authentifiziert werden.", 400)
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
        if "data" in self._dict:
            # If data is present, return a response with the data
            return jsonify({"data": self._dict["data"]})
        else:
            # If there is a specific message, get the corresponding message and status code
            message, status_code = self.select_message(self._dict["message"])

            if "meter_UID" in self._dict:
                # If a meter UID is present, include it in the response
                response = jsonify({"message": message, "meterUID": self._dict["meter_UID"]})
                response.status_code = status_code
                return response
            else:
                # Otherwise, return the message with the status code
                response = jsonify({"message": message})
                response.status_code = status_code
                return response