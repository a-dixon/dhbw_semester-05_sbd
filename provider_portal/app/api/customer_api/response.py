import sys
from flask import jsonify


class Response:
    MESSAGES = {
        "success": ("Aktion erfolgreich durchgeführt", 200),
        "error_database": ("Es ist ein Fehler in der Datenbank aufgetreten.", 500),
        "error_authentication": ("Customer Portal konnte nicht authentifiziert werden.", 400)
    }


    # boolean_patterns: bool[0]: auth status (successful --> true), bool[1] database status (successful --> true)
    def __init__(self, boolean_patterns):
        self.boolean_patterns = boolean_patterns
        self.message, self.status_code = self.select_message()


    def select_message(self):
        if not self.boolean_patterns[0]:
            return Response.MESSAGES.get("error_authentication")
        elif not self.boolean_patterns[1]:
            return Response.MESSAGES.get("error_database")
        else:
            return Response.MESSAGES.get("success")


    def to_response(self):
        response = jsonify({"message": self.message})
        response.status_code = self.status_code
        return response
    