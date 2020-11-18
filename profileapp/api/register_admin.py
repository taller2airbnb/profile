from flask import request, Blueprint, jsonify
from flask_expects_json import expects_json
from profileapp.api.user import register_new_user
from profileapp.api.utils import validate_user_is_admin, get_id_profile_from_description
from flasgger.utils import swag_from
from profileapp.Errors.ProfileAppException import ProfileAppException
from flask import current_app

schema_new_admin = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string'},
        'national_id': {'type': 'string'},
        'national_id_type': {'type': 'string'},
        'alias': {'type': 'string'},
        'password': {'type': 'string'},
        'user_logged_id': {'type': 'integer'}
    },
    'required': ['first_name', 'last_name', 'email', 'national_id', 'national_id_type',
                 'alias', 'password', 'user_logged_id']}

bp_register_admin = Blueprint('register_admin', __name__, url_prefix='/register_admin/')


@bp_register_admin.route("/", methods=['POST'])
@expects_json(schema_new_admin)
@swag_from(methods=['POST'])
def register_new_admin():
    """
    Register a new user
    The new user has to fulfill all the required fields
    ---
    tags:
      - registration
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
            required:
              - first_name
              - last_name
              - email
              - national_id
              - national_id_type
              - alias
              - password
              - user_logged_id
            properties:
              first_name:
                type: string
                description: First name of the new user
              last_name:
                type: string
                description: Last name of the new user
              email:
                type: string
                description: Unique email representing the new user
              national_id:
                type: string
                description: National ID of the new user
              national_id_type:
                type: string
                description: National ID Type of the new user
              alias:
                type: string
                description: Unique alias representing the new user
              password:
                type: string
                description: Password of the new user
              user_logged_id:
                type: integer
                description: Id of the user that creates the admin.
    responses:
      200:
        description: A successful profile creation
        schema:
          properties:
              email:
                type: string
                description: Unique email of the created user
              alias:
                type: string
                description: Unique alias of the created user
              id:
                type: integer
                description: Unique identifier of the created user
              name:
                type: string
                description: Name of the created user
    """
    # @expects_json(schema_new_user), just like register
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data
    post_data = request.get_json()
    current_app.logger.info("Registering admin " + post_data['email'])
    try:
        validate_user_is_admin(post_data['user_logged_id'])
        post_data['profile'] = get_id_profile_from_description('admin')
    except ProfileAppException as e:
        current_app.logger.error("Admin registration for " + post_data['email'] + "failed.")
        return jsonify({'Error': e.message}), 400

    current_app.logger.info("Admin registration for " + post_data['email'] + "succeeded.")
    return register_new_user()
