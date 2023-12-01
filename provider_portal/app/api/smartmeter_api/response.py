import sys
from flask import jsonify

class Response:
    """
    Class to generate Flask responses based on boolean patterns representing authentication and database status.
    """

    # Define messages and their corresponding HTTP status codes
    MESSAGES = {
        "success": ("Die Messpunkte wurden erfolgreich in die Datenbank geschrieben.", 200),
        "error_database": ("Die Messpunkte konnten nicht in die Datenbank geschrieben werden.", 500),
        "error_decoding": ("Das Format konnte nicht dekodiert werden.", 400),
        "error_certificate": ("Smart Meter Zertifikat nicht am API Endpoint hinterlegt.", 400)
    }

    def __init__(self, boolean_patterns):
        """
        Initializes the Response object.

        Args:
            boolean_patterns (list): List of boolean values representing authentication and database status.
        """
        self.boolean_patterns = boolean_patterns
        self.message, self.status_code = self.select_message()

    def select_message(self):
        """
        Selects the appropriate message and HTTP status code based on boolean patterns.

        Returns:
            tuple: Tuple containing message and HTTP status code.
        """
        if not self.boolean_patterns[0]:
            return Response.MESSAGES.get("error_certificate")
        elif not self.boolean_patterns[1]:
            return Response.MESSAGES.get("error_database")
        else:
            return Response.MESSAGES.get("success")

    def to_response(self):
        """
        Converts the Response object to a Flask response.

        Returns:
            Response: Flask response containing the selected message and HTTP status code.
        """
        response = jsonify({"message": self.message})
        response.status_code = self.status_code
        return response