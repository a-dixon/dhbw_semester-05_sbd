import logging
import sys

from flask import request, json
from .admin_api import AdminAPI
from .response import Response
from . import admin_api_blueprint as bp
from app.utils.validation.string_validation import input_validation


logger = logging.getLogger("main")


@bp.route('customer-create', methods=['POST'])
def create_customer_portal():
    """
    Route to create a new customer portal from the admin CLI.

    This route is used by administrators to create a new customer portal. The request body must include
    the administrator's API key and the desired username for the new customer portal.

    Returns:
        JSON response containing the result of the operation:
        - If successful, returns a success message along with the generated customer UID and API key.
        - If unsuccessful, returns an error message.
    """
    # --- Extract data from request body ---
    try:
        data = json.loads(request.data)
        api_key = data["api_key"]
        username = data["username"]

        if input_validation([api_key, username]):
            # Initialize AdminAPI class
            api = AdminAPI(api_key=api_key, username=username)
            auth_status = api.authenticate_admin_user()
        else:
            raise ValueError("error_decoding")
    except Exception as err:
        logger.error(f"An error has occurred when creating a customer: {err}")
        res = {"message": "error_decoding"}
        return Response(dict=res).create_response()

    if auth_status:
        try:
            customer_UID, customer_api_key = api.create_customer_portal()
            res = {"message": "success_create_customer", "customer_UID": customer_UID,
                   "customer_api_key": customer_api_key}
            return Response(dict=res).create_response()

        except:
            res = {"message": "error_create_customer"}
            return Response(dict=res).create_response()
    res = {"message": "error_authentication"}
    return Response(dict=res).create_response()


@bp.route('customer-delete', methods=['DELETE'])
def delete_customer_portal():
    """
    Route to delete a customer portal from the admin CLI.

    This route is used by administrators to delete a customer portal based on the provided customer UID.

    Returns:
        JSON response containing the result of the operation:
        - If successful, returns a success message.
        - If unsuccessful, returns an error message.
    """
    try:
        data = json.loads(request.data)
        api_key = data["api_key"]
        username = data["username"]
        customer_UID = data['customer_UID']

        if input_validation([api_key, username, customer_UID]):
            # Initialize AdminAPI class
            api = AdminAPI(api_key=api_key, username=username)
            auth_status = api.authenticate_admin_user()
        else:
            raise ValueError("error_decoding")
    except Exception as err:
        logger.error(f"An error has occurred when deleting a customer: {err}")
        res = {"message": "error_decoding"}
        return Response(dict=res).create_response()

    if auth_status:
        try:
            api.delete_customer_portal(customer_UID)
            res = {"message": "success_delete_customer"}
            return Response(dict=res).create_response()

        except Exception as err:
            logger.error(f"An error has occurred when deleting a customer: {err}")
            res = {"message": "error_delete_customer"}
            return Response(dict=res).create_response()

    res = {"message": "error_authentication"}
    return Response(dict=res).create_response()


@bp.route('customer-list', methods=['GET'])
def list_customer_portals():
    """
    Route to list all customer portals.

    This route is used by administrators to get a list of all customer portals.

    Returns:
        JSON response containing the list of customer portals.
    """
    try:
        data = json.loads(request.data)
        api_key = data["api_key"]
        username = data["username"]
        if input_validation([api_key, username]):
            # Initialize AdminAPI class
            api = AdminAPI(api_key=api_key, username=username)
            auth_status = api.authenticate_admin_user()
        else:
            raise ValueError("error_decoding")
    except Exception as err:
        logger.error(f"An error has occurred when listing customer portals: {err}")
        res = {"message": "error_authentication"}
        return Response(dict=res).create_response()

    if auth_status:
        try:
            customer_portals = api.list_customer_portals()
            res = {"message": "success_list_customer_portals", "customer_portals": customer_portals}
            return Response(dict=res).create_response()

        except Exception as err:
            logger.error(f"An error has occurred when listing customer portals: {err}")
            res = {"message": "error_list_customer_portals"}
            return Response(dict=res).create_response()

    res = {"message": "error_authentication"}
    return Response(dict=res).create_response()


@bp.route('meter-list', methods=['GET'])
def list_smart_meters_for_customer():
    """
    Route to list all smart meters of customer.

    This route is used by administrators to get a list of all smart meters of customer.

    Returns:
        JSON response containing the list of smart meters.
    """
    try:
        data = json.loads(request.data)
        api_key = data["api_key"]
        username = data["username"]
        customer_UID = data["customer_UID"]
        if input_validation([api_key, username]):
            # Initialize AdminAPI class
            api = AdminAPI(api_key=api_key, username=username)
            auth_status = api.authenticate_admin_user()
        else:
            raise ValueError("error_decoding")
    except Exception as err:
        logger.error(f"An error has occurred when listing smart meters: {err}")
        res = {"message": "error_authentication"}
        return Response(dict=res).create_response()

    if auth_status:
        try:
            meters = api.list_smart_meters_for_customer(customer_UID)
            res = {"message": "success_list_smart_meters", "meters": meters}
            return Response(dict=res).create_response()

        except Exception as err:
            logger.error(f"An error has occurred when listing smart meters: {err}")
            res = {"message": "error_list_smart_meters"}
            return Response(dict=res).create_response()

    res = {"message": "error_authentication"}
    return Response(dict=res).create_response()
