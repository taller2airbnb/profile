import secrets

from flasgger.utils import swag_from
from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request

from profileapp import database
from profileapp.api.api_validator import require_appkey
from profileapp.model import APIKeyToken

bp_apikey = Blueprint('apikey', __name__, url_prefix='/apikey/')


@bp_apikey.route("/add/", methods=['POST'])
@require_appkey
@swag_from(methods=['POST'])
def add_new_apikey():
    """
    Create a new apikey
    name_from is needed
    ---
    tags:
      - apikey
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
            required:
              - name_from
            properties:
              name_from:
                type: string
                description: representing a apikey name_from
    security:
      - APIKeyHeader: ['Token']
    responses:
      200:
        description: A successful apikey creation
        schema:
          properties:
              id:
                type: integer
                description: Unique identifier representing a apikey name_from
              name_from:
                type: string
                description: representing a apikey name_from
    """
    post_data = request.get_json()

    current_app.logger.info('Creating new apikey: ' + post_data['name_from'])
    apitoken = str(secrets.token_urlsafe(16))
    apikey = APIKeyToken(name_from=post_data['name_from'], api_key_token=apitoken, active=True)

    try:
        # add to the database session
        database.db.session.add(apikey)

        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error('APIKeyToken creation failed: apikey with ' + str(post_data['name_from']) + ' already exists.')
        return jsonify({'Error': "apikey already exists"}), 400

    current_app.logger.info('APIKeyToken ' + post_data['name_from'] + ' successfully created.')
    return jsonify({'name_from': apikey.name_from, 'api_key_token':apitoken}), 200


@bp_apikey.route("/", methods=['GET'])
@require_appkey
@swag_from(methods=['GET'])
def get_all_apikey():
    """
    Get all apikey
    APIKeyToken id and name_from is going to be given
    ---
    tags:
      - apikey
    security:
      - APIKeyHeader: ['Token']
    responses:
      200:
        description: A list of apikey created
    """
    # Get all apikey
    apikey = APIKeyToken.query.all()
    profile_list = []
    for apikey in apikey:
        profile_object = {
            'id': apikey.id,
            'name_from': apikey.name_from,
            'api_key_token': apikey.api_key_token,
            'active': apikey.active
        }
        profile_list.append(profile_object)
    response_object = {
        'apikeys': profile_list
    }
    return jsonify(response_object), 200


@bp_apikey.route("/<int:id_apikey>/active_status", methods=['PUT'])
@require_appkey
@swag_from(methods=['PUT'])
def new_status_apikey(id_apikey):
    """
    Change apikey Active status
    ---
    tags:
      - apikey
    consumes:
      - application/json
    parameters:
      - in: path
        name: id_apikey
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
            required:
              - active
            properties:
              active:
                type: boolean
                description: New active STATUS
    security:
      - APIKeyHeader: ['Token']
    responses:
      200:
        description: A successful change of apikey active status.
        schema:
          properties:
              user_id:
                type: integer
                description: Unique identifier representing the apikey
              push_token:
                type: string
                description: token
    """
    post_data = request.get_json()

    apikey = APIKeyToken.query.filter_by(id=id_apikey).first()

    current_app.logger.info('Modification in apikey: ' + apikey.name_from)

    new_status = (request.get_json())['active']

    apikey.active = new_status

    try:
        # add to the database session
        database.db.session.add(apikey)

        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error('APIKeyToken creation failed: apikey with ' + str(post_data['name_from']) + ' already exists.')
        return jsonify({'Error': "apikey already exists"}), 400

    current_app.logger.info('APIKeyToken ' + apikey.name_from + ' successfully modified.')
    return jsonify({'name_from': apikey.name_from, 'api_key_status': apikey.active}), 200
