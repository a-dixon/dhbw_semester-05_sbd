from flask import request, json, jsonify
from . import customer_api_blueprint as bp
from customer_api import CustomerAPI
from response import Response


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
            status_1 = True
            status_2 = False
        except:
            status_1 = False
            status_2 = False
    
    return Response([auth_status, status_1, status_2], meter_UID=meter_UID).to_response()


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
    res = api.get_meter_measurements(start_time, end_time, data_interval, meter_UID)

    pass


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
            create_status = True
            delete_status = True
        except:
            create_status = False
            delete_status = True

    return Response([auth_status, create_status, delete_status], meter_UID=meter_UID).to_response()
