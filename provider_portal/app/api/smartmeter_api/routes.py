from . import smartmeter_api_blueprint as bp


@bp.route('meter-measurements', methods=['POST'])
def meter_measurements():
    return "Hallo"

