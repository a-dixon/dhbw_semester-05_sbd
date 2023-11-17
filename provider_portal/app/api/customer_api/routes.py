import sys

from flask import request, json, jsonify
from . import customer_api_blueprint as bp
from .customer_api import CustomerAPI
from .response import Response


@bp.route('meter-create', methods=['POST'])
def create_meter():
    ''' Route to create meter.'''
    # Extract api key
    api_key = request.headers['Authorization']

    # Extract data from request body
    data = json.loads(request.data)
    customer_UID = data['customerUID']

    # Initiate customer api class
    api = CustomerAPI(customer_UID=customer_UID, api_key=api_key)
    auth_status = api.authenticate_customer_portal()

    if auth_status:
        try:
            meter_UID = api.create_meter()
            res = {"message": "success_create_meter", "meter_UID": meter_UID}
            print(res, file=sys.stderr)
            return Response(dict=res).create_response()

        except:
            res = {"message": "error_create_meter"}
            return Response(dict=res).create_response()

    res = {"message": "error_authentication"}
    return Response(dict=res).create_response()


@bp.route('meter-measurements', methods=['GET'])
def meter_measurements():
    ''' Route to get meter-measurements'''
    # Extract api key
    api_key = request.headers['Authorization']

    # Extract data from request body
    customer_UID = request.args.get('customerUID')
    meter_UID = request.args.get('meterUID')
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')
    data_interval = request.args.get('dataInterval')

    api = CustomerAPI(customer_UID=customer_UID, api_key=api_key)
    auth_status = api.authenticate_customer_portal()

    if auth_status:
        try:
            measurements = api.get_meter_measurements(start_time, end_time, data_interval, meter_UID)
            res = {"data": measurements}
            return Response(dict=res).create_response()
        except ValueError as err:
            res = {"message": f"{err}"}
            return Response(dict=res).create_response()
        except Exception as err:
            print(err, file=sys.stderr)
            res = {"message": "error_decoding"}
            return Response(dict=res).create_response()

    res = {"message": "error_authentication"}
    return Response(dict=res).create_response()


@bp.route('meter-delete', methods=['DELETE'])
def delete_meter():
    ''' Route to delete meter'''
    # Extract api key
    api_key = request.headers['Authorization']

    # Extract data from request body
    data = json.loads(request.data)
    customer_UID = data['customerUID']
    meter_UID = data['meterUID']

    api = CustomerAPI(customer_UID=customer_UID, api_key=api_key)
    auth_status = api.authenticate_customer_portal()

    if auth_status:

        try:
            api.delete_meter(meter_UID=meter_UID)
            res = {"message": "success_delete_meter"}
            return Response(dict=res).create_response()

        except:
            res = {"message": "error_meter_customer_combination"}
            return Response(dict=res).create_response()

    res = {"message": "error_authentication"}
    return Response(dict=res).create_response()
