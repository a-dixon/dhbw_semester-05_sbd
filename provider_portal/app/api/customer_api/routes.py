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
    data = json.loads(request.data)
    customer_UID = data['customerUID']
    meter_UID = data['meterUID']
    start_time = data['startTime']
    end_time = data['endTime']
    data_interval = data['dataInterval']

    api = CustomerAPI(customer_UID=customer_UID, api_key=api_key)
    auth_status = api.authenticate_customer_portal()

    if auth_status:

        res = api.get_meter_measurements(start_time, end_time, data_interval, meter_UID)
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
            api.delete_meter()
            status_1 = True
            status_2 = True
        except:
            status_1 = False
            status_2 = True

    return Response([auth_status, status_1, status_2]).to_response()
