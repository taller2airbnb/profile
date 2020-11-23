import hashlib
import json

import requests
from flask import current_app
from flask import jsonify
from flask import request

from profileapp import database
from profileapp.Errors.ProfileAppException import ProfileAppException
from profileapp.api import GOOGLE_VALIDATOR, USER_ADMIN, USER_BOOKBNB, USER_GOOGLE
from profileapp.api.utils import validate_existent_profile_id, validate_free_user_identifiers, validate_user_password, \
    validate_user_type, \
    validate_user_is_admin, get_id_profile_from_description, validate_google_response
from profileapp.model import Users, ProfileUser

schema_new_user = {
    'type': 'object',
    'properties': {
        'user_type': {'type': 'string'},
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string'},
        'national_id': {'type': 'string'},
        'national_id_type': {'type': 'string'},
        'alias': {'type': 'string'},
        'password': {'type': 'string'},
        'profile': {'type': 'integer'},
        'google_token': {'type': 'string'},
        'user_logged_id': {'type': 'integer'}
    },
    'required': ['user_type', 'profile']}


def register_new_user():
    """
    Register a new user
    The new user has to fulfill the required fields by type
    ---
    tags:
      - user
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
            required:
              - user_type
              - first_name
              - last_name
              - email
              - national_id
              - national_id_type
              - alias
              - password
              - profile
              - google_token
            properties:
              user_type:
                type: string
                description: REQUIRED - Type of user in registration - BookBnb, Admin or GoogleUser
              first_name:
                type: string
                description: First name of the new user - BookBnb, Admin
              last_name:
                type: string
                description: Last name of the new user - BookBnb, Admin
              email:
                type: string
                description: Unique email representing the new user - BookBnb, Admin
              national_id:
                type: string
                description: National ID of the new user - BookBnb, Admin
              national_id_type:
                type: string
                description: National ID Type of the new user - BookBnb, Admin
              alias:
                type: string
                description: Unique alias representing the new user - BookBnb, Admin
              password:
                type: string
                description: Password of the new user - BookBnb, Admin
              profile:
                type: integer
                description: REQUIRED - Profile of the new user, has to be an existing one (check /profiles/) - All Type of Users
              google_token:
                type: string
                description: identifier representing a google user - GoogleUser
              user_logged_id:
                type: integer
                description: Id of the user that creates the admin. - Admin
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
    # @expects_json(schema_new_user)
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data
    post_data = request.get_json()
    user_type = post_data['user_type']

    try:
        validate_user_type(user_type)

        if user_type.lower() == USER_ADMIN:
            return register_admin_user(post_data)

        if user_type.lower() == USER_BOOKBNB:
            return register_bookbnb_user(post_data)

        if user_type.lower() == USER_GOOGLE:
            return register_google_user(post_data)

    except ProfileAppException as e:
        current_app.logger.error("Registration for user failed.")
        return jsonify({'Error': e.message}), e.error_code


def register_admin_user(post_data):
    validate_user_is_admin(post_data['user_logged_id'])
    post_data['profile'] = get_id_profile_from_description('admin')
    return register_bookbnb_user(post_data)


def register_bookbnb_user(post_data):
    current_app.logger.info("Registering user " + post_data['email'])

    validate_existent_profile_id(post_data['profile'])
    validate_free_user_identifiers(post_data['email'], post_data['alias'])
    validate_user_password(post_data['password'])

    password = hashlib.md5(post_data['password'].encode()).hexdigest()

    user = Users(first_name=post_data['first_name'], last_name=post_data['last_name'], email=post_data['email'],
                 national_id=post_data['national_id'], national_id_type=post_data['national_id_type'],
                 alias=post_data['alias'], password=password)

    attempt = create_user_in_db(database.db.session, user, post_data)
    if not attempt:
        return attempt

    current_app.logger.info("Registration for user " + post_data['email'] + "succeeded.")
    return jsonify({'id': user.id_user, 'name': user.first_name, 'alias': user.alias, 'email': user.email}), 200


def register_google_user(post_data):
    headers = {
        "Authorization": "Bearer " + str(post_data['google_token'])
    }
    response = requests.get(GOOGLE_VALIDATOR, headers=headers)
    response_json = json.loads(response.content)
    print(response_json)

    validate_google_response(response_json)
    email = response_json['email']
    last_name = response_json['family_name']
    first_name = response_json['given_name']
    alias = response_json['name']

    validate_existent_profile_id(post_data['profile'])
    validate_free_user_identifiers(email)

    user = Users(first_name=first_name, last_name=last_name, email=email, alias=alias)

    attempt = create_user_in_db(database.db.session, user, post_data)
    if not attempt:
        return attempt

    current_app.logger.info("Google registration for user " + email + "succeeded.")
    return jsonify({'Token Validated': 'Ok', 'id': user.id_user, "Email": email}), 200


def create_user_in_db(db, user, post_data):
    try:
        # add to the database session
        database.db.session.add(user)

        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error("Something happened creating the user " + user.email + "in the database.")
        return jsonify({'Error': "Something happened creating the User in the Database"}), 400

    user_created = Users.query.filter_by(email=user.email).first()
    profile_user = ProfileUser(id_user=user_created.id_user, id_profile=post_data['profile'])

    attempt = create_profile_user_in_db(database.db.session, profile_user, post_data)
    if not attempt:
        return attempt

    return True


def create_profile_user_in_db(db, profile_user, post_data):
    try:
        # add to the database session
        database.db.session.add(profile_user)

        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error(
            "Something happened creating the Profile-User relation for user " + post_data['email'] + "in the database.")
        return jsonify({'error': "Something happened creating the Profile-User relation in the Database"}), 400

    return True
