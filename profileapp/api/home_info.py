import requests
from flask import Blueprint
from flask import jsonify, render_template
from flasgger.utils import swag_from

from profileapp.api.api_validator import require_appkey

bp_homeinfo = Blueprint('status_info', __name__, url_prefix='/')


@bp_homeinfo.route("/", methods=['GET'])
@swag_from(methods=['GET'])
def home():

    return render_template("home.html")


@bp_homeinfo.route("/business-status")
@require_appkey
@swag_from(methods=['GET'])
def business():
    """
    BusinessCore Health Check
    To Know if the BusinessCore Service is UP and running.
    ---
    tags:
      - health
    security:
      - APIKeyHeader: ['Token']
    responses:
      200:
        description: Status
    """
    response = requests.get('https://taller2airbnb-businesscore.herokuapp.com/health')
    return response.json()


@bp_homeinfo.route("/health", methods=['GET'])
@swag_from(methods=['GET'])
def health():
    """
    Health Check
    To Know if the APP is UP and running.
    ---
    tags:
      - health
    security:
      - APIKeyHeader: ['Token']
    responses:
      200:
        description: Status
    """
    return jsonify({"status": "UP", "from": "Profile"}), 200
