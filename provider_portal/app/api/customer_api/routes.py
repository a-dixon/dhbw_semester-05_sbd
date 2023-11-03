from . import customer_api_blueprint as bp

@bp.route('meter-create', methods=['POST'])
def create_meter():
    pass

@bp.route('meter-measurements', methods=['GET'])
def meter_measurements():
    pass

@bp.route('meter-delete', methods=['DELETE'])
def delete_meter():
    pass
