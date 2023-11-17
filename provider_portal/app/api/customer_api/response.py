import sys
from flask import jsonify


class Response:
    MESSAGES = {
        "success_create_meter": ("Smart Meter wurde erfolgreich angelegt.", 201),
        "error_create_meter": ("Smart Meter konnte nicht angelegt werden. Die Kombination von Meter UID und Customer UID existiert bereits.", 409),

        "success_delete_meter": ("Smart Meter wurde erfolgreich gelöscht.", 200),
        "error_delete_meter": ("Die Kombination von Meter UID und Customer UID existiert nicht.", 404),

        "error_authentication": ("Customer Portal konnte nicht authentifiziert werden.", 400)
    }


    # boolean_patterns: bool[0]: auth status (successful --> true), bool[1] database status (successful --> true)
    def __init__(self, boolean_patterns, meter_UID):
        self.boolean_patterns = boolean_patterns
        self.message, self.status_code = self.select_message()
        if meter_UID:
            self.meter_UID = meter_UID


    def select_message(self):
        if not self.boolean_patterns[0]:
            return Response.MESSAGES.get("error_authentication")
        
        # --- Create Status False ---
        elif not self.boolean_patterns[1] and not self.boolean_patterns[2]:
            return Response.MESSAGES.get("error_create_meter")
        
        # --- Create Status True ---
        elif self.boolean_patterns[1] and not self.boolean_patterns[2]:
            return Response.MESSAGES.get("success_create_meter")
        
        # --- Delete Status False ---
        elif not self.boolean_patterns[1] and self.boolean_patterns[2]:
            return Response.MESSAGES.get("error_delete_meter")

        # --- Delete Status True ---
        elif self.boolean_patterns[1] and self.boolean_patterns[2]:
            return Response.MESSAGES.get("success_delete_meter")


    def to_response(self):
        if self.meter_UID:
            response = jsonify({"message": self.message, "meterUID": self.meter_UID})
        else:
            response = jsonify({"message": self.message})
        response.status_code = self.status_code
        return response
    