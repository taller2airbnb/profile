import json
import requests
from profileapp import database
from profileapp.model import Users, ProfileUser
from flask import request
from flask import Blueprint
from flask import jsonify
from flask_expects_json import expects_json
from profileapp.api.utils import validate_user_password, validate_existent_user_by_mail, validate_free_user_identifiers, \
    validate_existent_profile_id
from flasgger.utils import swag_from
from profileapp.Errors.ProfileAppException import ProfileAppException

GOOGLE_VALIDATOR = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"

schema_new_user_from_google = {
    'type': 'object',
    'properties': {
        'token': {'type': 'string'},
        'profile': {'type': 'integer'}
    },
    'required': ['token', 'profile']}

schema_user_login_from_google = {
    'type': 'object',
    'properties': {
        'token': {'type': 'string'},
    },
    'required': ['token']}

bp_google_auth = Blueprint('google_auth', __name__, url_prefix='/google_auth/')


@bp_google_auth.route("/register", methods=['POST'])
@swag_from(methods=['POST'])
@expects_json(schema_new_user_from_google)
def google_register():
    """
    Register
    Existent user is needed
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
              - token
              - profile
            properties:
              token:
                type: string
                description: identifier representing a google user
              profile:
                type: integer
                description: identifier representing a profile
    responses:
      200:
        description: A successful profile creation
        schema:
          properties:
              token:
                type: string
                description: identifier representing a google user
    """
    # @expects_json(schema_new_user)
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data
    post_data = request.get_json()
    #headers = {
    #    "Authorization": "Bearer ya29.A0AfH6SMAMtWS8VaxlJZDzMpUu5WxAS0TgqOToAtWZDYHkoEHQfo86Y-s9ZiFCZHiHUss4Fv4KDCbLq4VSwRNXklgV2s6soBeaYDePpta7jk4Z31E4inq6jt7kVvYHsvvMpuusKCgj9AksmoiWSURDZT_7j8-b-pfM4sO0wrxz1QA"
    #}
    headers = {
        "Authorization": "Bearer " + str(post_data['token'])
    }
    response = requests.get(GOOGLE_VALIDATOR, headers=headers)
    response_json = json.loads(response.content)
    if "error" in response_json:
        return jsonify({'Error Received': 'Not able to validate token with GoogleAPI'}), 400
    else:
        email = response_json['email']
        last_name = response_json['family_name']
        first_name = response_json['given_name']
        alias = response_json['name']
        try:
            validate_existent_profile_id(post_data['profile'])
            validate_free_user_identifiers(email)
        except ProfileAppException as e:
            return jsonify({'Error': e.message}), e.error_code
        user = Users(first_name=first_name, last_name=last_name, email=email, alias=alias)
        try:
            # add to the database session
            database.db.session.add(user)
            # commit to persist into the database
            database.db.session.commit()
        except:
            return jsonify({'Error': "Something happened creating the User in the Database"}), 400

        user_created = Users.query.filter_by(email=email).first()
        profile_user = ProfileUser(id_user=user_created.id_user, id_profile=post_data['profile'])
        try:
            # add to the database session
            database.db.session.add(profile_user)

            # commit to persist into the database
            database.db.session.commit()
        except:
            return jsonify({'error': "Something happened creating the Profile-User relation in the Database"}), 400

        return jsonify({'Token Validated': 'Ok', 'id': user.id_user}), 200


@bp_google_auth.route("/login", methods=['POST'])
@swag_from(methods=['POST'])
@expects_json(schema_user_login_from_google)
def google_login():
    """
    login
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
              - token
            properties:
              token:
                type: string
                description: identifier representing a google user
    responses:
      200:
        description: A successful profile creation
        schema:
          properties:
              token:
                type: string
                description: identifier representing a google user
    """
    # @expects_json(schema_new_user)
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data
    post_data = request.get_json()
    headers = {
        "Authorization": "Bearer " + str(post_data['token'])
    }
    response = requests.get(GOOGLE_VALIDATOR, headers=headers)
    response_json = json.loads(response.content)
    if "error" in response_json:
        return jsonify({'Error Received': 'Not able to validate token with GoogleAPI'}), 400
    else:
        email = response_json['email']
        try:
            validate_existent_user_by_mail(email)
        except ProfileAppException as e:
            return jsonify({'Error': e.message}), e.error_code

        user = Users.query.filter_by(email=email).first()
        if user.password is not None:
            return jsonify({'Error': 'User register without Google Auth'}), 400

        return jsonify({'Token Validated': 'Ok', 'id': user.id_user}), 200
