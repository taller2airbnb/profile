from profileapp.model import Users, ProfileUser
from flask import request
from flask import Blueprint
from flask import jsonify
from flask_expects_json import expects_json
from profileapp.api.utils import validate_user_password, validate_existent_user_by_mail, validate_google_response, \
    validate_user_type, validate_is_google_user
from flasgger.utils import swag_from
from profileapp.Errors.ProfileAppException import ProfileAppException
from flask import current_app
import json
import requests
from profileapp.api import GOOGLE_VALIDATOR, USER_GOOGLE

schema_login_user = {
    'type': 'object',
    'properties': {
        'user_type': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'google_token': {'type': 'string'},
    },
    'required': ['user_type']}

bp_login = Blueprint('login', __name__, url_prefix='/login/')


@bp_login.route("/", methods=['POST'])
@swag_from(methods=['POST'])
@expects_json(schema_login_user)
def login():
    """
    Login
    Existent user is needed
    ---
    tags:
      - login
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
            required:
              - user_type
            properties:
              user_type:
                type: string
                description: REQUIRED - Type of user in registration - BookBnb, Admin or GoogleUser
              email:
                type: string
                description: Unique identifier representing a existent user - BookBnb, Admin
              password:
                type: string
                description: password of the user - BookBnb, Admin
              google_token:
                type: string
                description: identifier representing a google user - GoogleUser
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
              profile_id:
                type: integer
                description: Unique identifier of the profile created user
              name:
                type: string
                description: Name of the created user
    """
    # @expects_json(schema_new_user)
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data
    post_data = request.get_json()
    user_type = post_data['user_type']

    try:
        validate_user_type(user_type)

        if user_type.lower() == USER_GOOGLE:
            return login_google_user(post_data)
        else:
            return login_bookbnb_user(post_data)

    except ProfileAppException as e:
        current_app.logger.info("Login for a " + user_type + "user failed.")
        return jsonify({'Error': e.message}), e.error_code


def login_google_user(post_data):
    headers = {
        "Authorization": "Bearer " + str(post_data['google_token'])
    }
    response = requests.get(GOOGLE_VALIDATOR, headers=headers)
    response_json = json.loads(response.content)
    validate_google_response(response_json)
    email = response_json['email']

    validate_existent_user_by_mail(email)

    user = Users.query.filter_by(email=email).first()

    validate_is_google_user(user)

    return jsonify({'Token Validated': 'Ok', 'id': user.id_user, "Mail": user.email}), 200


def login_bookbnb_user(post_data):
    current_app.logger.info("Attempting login for " + post_data['email'])

    validate_existent_user_by_mail(post_data['email'])

    user = Users.query.filter_by(email=post_data['email']).first()

    validate_user_password(post_data['password'], user.password)

    profile_user = ProfileUser.query.filter_by(id_user=user.id_user).first()

    current_app.logger.info("Login " + post_data['email'] + " successful.")

    return jsonify({'id': user.id_user, 'name': user.first_name, 'alias': user.alias, 'email': user.email,
                    'profile': profile_user.id_profile}), 200
