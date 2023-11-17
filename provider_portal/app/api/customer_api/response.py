import sys
from flask import jsonify


class Response:
    MESSAGES = {
        "success_create_meter": ("Smart Meter wurde erfolgreich angelegt.", 201),
        "success_delete_meter": ("Smart Meter wurde erfolgreich gelöscht.", 200),

        "error_create_meter": ("Smart Meter konnte nicht angelegt werden. Die Kombination von Meter UID und Customer UID existiert bereits.", 409),
        "error_meter_customer_combination": ("Die Kombination von Meter UID und Customer UID existiert nicht.", 404),
        "error_no_data": ("Keine Daten im angegebenen Zeitraum vorhanden.", 404),
        "error_over_maximum": ("Die Anzahl der angeforderten Messpunkte überschreitet das Maximum. Bitte reduzieren Sie das Abfrageintervall oder teilen Sie die Anfrage auf.", 400),

        "error_authentication": ("Customer Portal konnte nicht authentifiziert werden.", 400)
    }


    def __init__(self, dict):
        self._dict = dict


    def select_message(self, message):
        return Response.MESSAGES.get(message)


    def create_response(self):
        if "data" in self._dict:
            return jsonify({"data": self._dict["data"]})
        
        else:
            message, status_code = self.select_message(self._dict["message"])

            if "meter_UID" in self._dict:
                response = jsonify({"message": message, "meterUID": self._dict["meter_UID"]})
                response.status_code = status_code
                return response

            else:
                response = jsonify({"message": self._dict["message"]})
                response.status_code = status_code
                return response
    