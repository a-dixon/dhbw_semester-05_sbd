from flask import request, json, jsonify
from . import customer_api_blueprint as bp
from . import customer_api


@bp.route('meter-create', methods=['POST'])
def create_meter():
    ''' Route to create meter.'''
    # Extract api key
    api_key = request.headers['Authorization']

    # Extract data from request body
    data = json.loads(request.data)
    customer_UID = data['customerUID']

    # Initiate customer api class
    api = customer_api(customer_UID=customer_UID, api_key=api_key)

    pass


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

    api = customer_api(customer_UID=customer_UID, api_key=api_key)
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

    api = customer_api(customer_UID=customer_UID, api_key=api_key)
    pass
