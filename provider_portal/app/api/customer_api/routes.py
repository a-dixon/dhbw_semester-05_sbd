import logging
import sys
import time

from flask import request, json, jsonify, g
from . import customer_api_blueprint as bp
from .customer_api import CustomerAPI
from .response import Response
from app.utils.validation.string_validation import input_validation


logger = logging.getLogger("main")

# Dictionary to store IP addresses, requests, and timestamps
request_tracker = {}


@bp.before_request
def before_request():
    """
    Function to check rate limit before each request.
    """
    # Extracting the IP address from the request
    ip_address = request.remote_addr

    # Initialize the request tracker for the IP address if not present
    request_tracker.setdefault(ip_address, {})

    # Removing entries older than 5 minutes
    current_time = time.time()
    request_tracker[ip_address] = {
        k: v for k, v in request_tracker[ip_address].items() if current_time - v <= 300
    }

    # Check if the IP has exceeded the maximum allowed requests
    if len(request_tracker.get(ip_address, {})) >= 300:
        res = {"message": "error_over_maximum"}
        return Response(dict=res).create_response()


@bp.route('meter-create', methods=['POST'])
def create_meter():
    """
    Route to create a meter.

    Expects a POST request with the following:
    - Headers: Authorization (API key)
    - JSON body: {"customerUID": "customer_unique_id"}

    Returns a JSON response with a message indicating the result.
    """
    try:
        # Extract API key from headers
        api_key = request.headers['Authorization']
        if "Bearer " in api_key:
            api_key = api_key.replace("Bearer ", "")

        # Extract data from the request body
        data = json.loads(request.data)
        customer_UID = data['customerUID']

        if input_validation(customer_UID):
            # Initialize CustomerAPI class
            api = CustomerAPI(customer_UID=customer_UID, api_key=api_key)
            auth_status = api.authenticate_customer_portal()
        else:
            raise ValueError("error_decoding")
    except Exception as err:
        logger.error(f"An error has occurred when creating a smart meter: {err}")
        res = {"message": "error_decoding"}
        return Response(dict=res).create_response()

    if auth_status:
        try:
            # Attempt to create a meter
            meter_UID = api.create_meter()
            res = {"message": "success_create_meter", "meter_UID": meter_UID}
            return Response(dict=res).create_response()
        except Exception as err:
            logger.error(f"An error has occurred when creating a smart meter: {err}")
            res = {"message": "error_create_meter"}
            return Response(dict=res).create_response()

    res = {"message": "error_authentication"}
    return Response(dict=res).create_response()


@bp.route('meter-measurements', methods=['GET'])
def meter_measurements():
    """
    Route to get meter measurements.

    Expects a GET request with the following query parameters:
    - customerUID: Customer unique ID
    - meterUID: Meter unique ID
    - startTime: Start time for data retrieval
    - endTime: End time for data retrieval
    - dataInterval: Data interval for aggregation

    Returns a JSON response with the requested meter measurements or an error message.
    """
    try:
        # Extract API key from headers
        api_key = request.headers['Authorization']
        if "Bearer " in api_key:
            api_key = api_key.replace("Bearer ", "")

        # Extract data from the request query parameters
        customer_UID = request.args.get('customerUID')
        meter_UID = request.args.get('meterUID')
        start_time = request.args.get('startTime')
        end_time = request.args.get('endTime')
        data_interval = request.args.get('dataInterval')

        if input_validation([customer_UID, meter_UID, start_time, end_time, data_interval]):
            # Initialize CustomerAPI class
            api = CustomerAPI(customer_UID=customer_UID, api_key=api_key)
            auth_status = api.authenticate_customer_portal()
        else:
            raise ValueError("error_decoding")
    except Exception as err:
        logger.error(f"An error has occurred within the get measurements: {err}")
        res = {"message": "error_decoding"}
        return Response(dict=res).create_response()

    if auth_status:
        try:
            # Attempt to retrieve meter measurements
            measurements = api.get_meter_measurements(start_time, end_time, data_interval, meter_UID)
            res = {"data": measurements}
            return Response(dict=res).create_response()
        except ValueError as err:
            # Handle specific error for no meter found
            res = {"message": f"{err}"}
            return Response(dict=res).create_response()
        except Exception as err:
            logger.error(f"An error has occurred within the get measurements: {err}")
            res = {"message": "error_decoding"}
            return Response(dict=res).create_response()

    res = {"message": "error_authentication"}
    return Response(dict=res).create_response()


@bp.route('meter-delete', methods=['DELETE'])
def delete_meter():
    """
    Route to delete a meter.

    Expects a DELETE request with the following:
    - Headers: Authorization (API key)
    - JSON body: {"customerUID": "customer_unique_id", "meterUID": "meter_unique_id"}

    Returns a JSON response with a message indicating the result.
    """
    try:
        # Extract API key from headers
        api_key = request.headers['Authorization']
        if "Bearer " in api_key:
            api_key = api_key.replace("Bearer ", "")

        # Extract data from the request body
        data = json.loads(request.data)
        customer_UID = data['customerUID']
        meter_UID = data['meterUID']

        if input_validation([customer_UID, meter_UID]):
            # Initialize CustomerAPI class
            api = CustomerAPI(customer_UID=customer_UID, api_key=api_key)
            auth_status = api.authenticate_customer_portal()
        else:
            raise ValueError("error_decoding")
    except Exception as err:
        logger.error(f"An error has occurred when deleting a smart meter: {err}")
        res = {"message": "error_decoding"}
        return Response(dict=res).create_response()

    if auth_status:
        try:
            # Attempt to delete a meter
            api.delete_meter(meter_UID=meter_UID)
            res = {"message": "success_delete_meter"}
            return Response(dict=res).create_response()
        except:
            res = {"message": "error_meter_customer_combination"}
            return Response(dict=res).create_response()

    res = {"message": "error_authentication"}
    return Response(dict=res).create_response()
