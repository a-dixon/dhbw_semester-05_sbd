from . import admin_api_blueprint as bp


@bp.route('test', methods=['POST'])
def create_meter():
    pass
