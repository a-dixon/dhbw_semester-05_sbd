import sys

import cryptography.x509
from cryptography.hazmat.backends import default_backend

from . import smartmeter_api_blueprint as bp
from flask import request, jsonify
from . import smartmeter_api


@bp.route('meter-measurements', methods=['POST'])
def meter_measurements():
    data = request.json

    client_cert_raw = request.environ.get("SSL_CLIENT_CERT")
    meter_uid = data["meterUID"]

    api = smartmeter_api.SmartmeterAPI(client_cert_raw, meter_uid)
    if api.authenticate_smartmeter():
        if api.add_measurements(data["data"]):
            response = jsonify({"message": "Die Messpunkte wurden erfolgreich in die Datenbank geschrieben"})
            response.status_code = 200
            return response
        else:
            response = jsonify({"message": "Die Messpunkte konnten nicht in die Datenbank geschrieben werden"})
            response.status_code = 500
            return response
    else:
        response = jsonify({"message": "Smart Meter Zertifikat nicht am API Endpoint hinterlegt"})
        response.status_code = 400
        return response
