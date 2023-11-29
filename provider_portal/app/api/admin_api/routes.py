import sys

from flask import request, json
from .admin_api import AdminAPI
from .response import Response
from . import admin_api_blueprint as bp


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
    data = json.loads(request.data)
    api_key = data['api_key']
    username = data['username']

    # --- Instantiate admin api class ---
    api = AdminAPI(api_key=api_key, username=username)
    auth_status = api.authenticate_admin_user()

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