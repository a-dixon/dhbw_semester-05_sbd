from app.api.smartmeter_api.response import Response
from . import smartmeter_api_blueprint as bp
from flask import request, jsonify
from . import smartmeter_api


@bp.route('meter-measurements', methods=['POST'])
def meter_measurements():
    data = request.json

    client_cert_raw = request.environ.get("SSL_CLIENT_CERT")
    meter_uid = data["meterUID"]

    api = smartmeter_api.SmartmeterAPI(client_cert_raw, meter_uid)
    auth_status = api.authenticate_smartmeter()
    db_status = False
    if auth_status:
        db_status = api.add_measurements(data["data"])

    return Response([auth_status, db_status]).to_response()
