import sys
from flask import jsonify


class Response:
    MESSAGES = {
        "success_create_customer": ("Customer Portal wurde erfolgreich angelegt.", 201),
        "error_create_customer": ("Customer Portal konnte nicht angelegt werden.", 409),
        "error_authentication": ("Admin User konnte nicht authentifiziert werden.", 400)
    }


    def __init__(self, dict):
        self._dict = dict


    def select_message(self, message):
        return Response.MESSAGES.get(message)


    def create_response(self):
        message, status_code = self.select_message(self._dict["message"])

        if "customer_UID" and "customer_api_key" in self._dict:
            response = jsonify({"message": message, "customer_UID": self._dict["customer_UID"], "customer_api_key": self._dict["customer_api_key"]})
            response.status_code = status_code
            return response

        else:
            response = jsonify({"message": message})
            response.status_code = status_code
            return response
    