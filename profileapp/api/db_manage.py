from flask import Blueprint
from flask import jsonify
from flasgger.utils import swag_from

from profileapp import model, database
from profileapp.api.api_validator import require_appkey

bp_db_manage = Blueprint('db', __name__, url_prefix='/db/')


@bp_db_manage.route("/restart", methods=['PUT'])
@require_appkey
@swag_from(methods=['PUT'])
def restart_db():
    """
    NOT WORKING - Restart DB to Default Values
    ---
    tags:
      - DB
    security:
      - APIKeyHeader: ['Token']
    responses:
      200:
        description: Status
    """

    # database.drop_and_create_tables()
    # model.insert_initial_values()

    return jsonify({"Nothing done"}), 200
