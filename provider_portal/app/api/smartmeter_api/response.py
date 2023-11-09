import sys

from flask import jsonify

class Response:
    MESSAGES = {
        "success": ("Die Messpunkte wurden erfolgreich in die Datenbank geschrieben", 200),
        "error_database": ("Die Messpunkte konnten nicht in die Datenbank geschrieben werden", 500),
        "error_certificate": ("Smart Meter Zertifikat nicht am API Endpoint hinterlegt", 400)
    }

    # boolean_patterns: bool[0]: auth status (successful --> true), bool[1] database status (successful --> true)
    def __init__(self, boolean_patterns):
        self.boolean_patterns = boolean_patterns
        self.message, self.status_code = self.select_message()


    def select_message(self):
        if not self.boolean_patterns[0]:
            return Response.MESSAGES.get("error_certificate")
        elif not self.boolean_patterns[1]:
            return Response.MESSAGES.get("error_database")
        else:
            return Response.MESSAGES.get("success")

    def to_response(self):
        response = jsonify({"message": self.message})
        response.status_code = self.status_code
        return response