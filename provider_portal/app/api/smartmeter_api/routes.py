import logging
import sys

from app.api.smartmeter_api.response import Response
from app.utils.validation.string_validation import input_validation
from . import smartmeter_api_blueprint as bp
from flask import request, jsonify
from . import smartmeter_api


logger = logging.getLogger("main")


@bp.route('meter-measurements', methods=['POST'])
def meter_measurements():
    """
    Endpoint for handling meter measurements from the smart meter.

    Expects a JSON payload with the following structure:
    {
        "meterUID": "unique_meter_id",
        "data": [
            {"timestamp": "2023-01-01T00:00:00Z", "value": 123.45},
            {"timestamp": "2023-01-01T01:00:00Z", "value": 456.78}
        ]
    }

    Returns a JSON response indicating authentication and database status.

    Authentication is based on the client certificate and meter UID.

    Returns:
        JSON: Response JSON containing authentication and database status.
    """
    try:
        data = request.json

        # Extract client certificate and meter UID from the request
        client_cert_raw = request.environ.get("SSL_CLIENT_CERT")
        meter_uid = data["meterUID"]

        if input_validation(meter_uid):
            api = smartmeter_api.SmartmeterAPI(client_cert_raw, meter_uid)
            auth_status = api.authenticate_smartmeter()
        else:
            raise ValueError("error_decoding")
    except Exception as err:
        logger.error(f"An error has occurred when getting meter measurements: {err}")
        res = {"message": "error_decoding"}
        return Response(dict=res).create_response()

    db_status = False
    # If authentication is successful, attempt to add measurements to the database
    if auth_status:
        db_status = api.add_measurements(data["data"])

    return Response([auth_status, db_status]).to_response()