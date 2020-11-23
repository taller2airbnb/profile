import hashlib
import json
import requests
from profileapp import database
from profileapp.model import Users, ProfileUser
from flask import request
from flask import Blueprint
from flask import jsonify
from flask_expects_json import expects_json
from profileapp.api.utils import validate_user_id_exists, validate_modify_schema_not_empty, \
    validate_existent_profile_id, validate_free_user_identifiers, validate_user_password, validate_user_type, \
    validate_user_is_admin, get_id_profile_from_description, validate_existent_user_by_mail, validate_google_response
from flasgger.utils import swag_from
from profileapp.Errors.ProfileAppException import ProfileAppException
from flask import current_app
from profileapp.api import GOOGLE_VALIDATOR, USER_ADMIN, USER_BOOKBNB, USER_GOOGLE

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

schema_modify_user = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'national_id': {'type': 'string'},
        'national_id_type': {'type': 'string'},
        'id': {'type': 'integer'}
    },
    'required': ['id']}

bp_user = Blueprint('user', __name__, url_prefix='/user/')


@bp_user.route("/", methods=['POST'])
@swag_from(methods=['POST'])
@expects_json(schema_new_user)
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


@bp_user.route("/", methods=['PUT'])
@swag_from(methods=['PUT'])
@expects_json(schema_modify_user)
def modify_user():
    """
    Modifies a user's name or national ID fields.
    No specific field is required but at least one must not be empty.
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
              - id
            properties:
              first_name:
                type: string
                description: New first name.
              last_name:
                type: string
                description: New last name.
              national_id:
                type: string
                description: New national id.
              national_id_type:
                type: string
                description: New national id type.
              id:
                type: integer
                description: Unique identifier for user whose fields will be modified.
    responses:
      200:
        description: A successful user modification.
        schema:
          properties:
              id:
                type: integer
                description: Unique identifier representing the user.
              modify_user:
                type: string
                description: Validation, expected 'Ok'.
    """
    # @expects_json(schema_new_user)
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data
    post_data = request.get_json()
    non_mandatory_fields = schema_modify_user['properties'].keys() - schema_modify_user['required']
    current_app.logger.info('Modifying user: ' + str(post_data['id']))

    try:
        validate_user_id_exists(post_data['id'])
        validate_modify_schema_not_empty(post_data, non_mandatory_fields)
    except ProfileAppException as e:
        current_app.logger.error("Modification for user " + str(post_data['id']) + " failed.")
        return jsonify({'Error': e.message}), e.error_code

    user = Users.query.filter_by(id_user=post_data['id']).first()

    if 'first_name' in post_data:
        # change first name
        user.first_name = post_data['first_name']
    if 'last_name' in post_data:
        # change last name
        user.last_name = post_data['last_name']
    if 'national_id' in post_data:
        # change national id
        user.national_id = post_data['national_id']
    if 'national_id_type' in post_data:
        # change national id type
        user.national_id_type = post_data['national_id_type']

    try:
        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error("Error when attempting to modify user " + str(post_data['id']) + " in the database.")
        return jsonify({'Error': "Something happened when attempting to modify user in the Database"}), 400

    current_app.logger.info("Modification for user with id " + str(post_data['id']) + " succeeded.")
    return jsonify({'id': user.id_user, 'modify_user': 'OK'}), 200


@bp_user.route("/<int:id>", methods=['GET'])
@swag_from(methods=['GET'])
def get_fields_from_user(id):
    """
    Get fields from user
    Profile id and description is going to be given
    ---
    tags:
      - user
    parameters:
      - in: path
        name: id
        type: integer
        required: false
    responses:
      200:
        description: A single user info
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
              first_name:
                type: string
                description: first name of the created user
              last_name:
                type: string
                description: last name of the created user
              national_id:
                type: string
                description: national id
              national_id_type:
                type: string
                description: national id type
    """
    current_app.logger.info('Getting info from user: ' + str(id))
    try:
        validate_user_id_exists(id)
    except ProfileAppException as e:
        current_app.logger.error("Getting info from user " + str(id) + " failed.")
        return jsonify({'Error': e.message}), e.error_code

    user = Users.query.filter_by(id_user=id).first()

    response_object = {
        'id': user.id_user,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'alias': user.alias,
        'email': user.email,
        'national_id': user.national_id,
        'national_id_type': user.national_id_type
    }
    current_app.logger.info('Obtained info from user: ' + str(id) + ' successfully.')
    return jsonify(response_object), 200


@bp_user.route("/", methods=['GET'])
@swag_from(methods=['GET'])
def get_fields_from_users():
    """
    Get fields from user
    Profile id and description is going to be given
    ---
    tags:
      - user
    parameters:
      - in: path
        name: id
        type: integer
        required: false
    responses:
      200:
        description: A single user info
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
              first_name:
                type: string
                description: first name of the created user
              last_name:
                type: string
                description: last name of the created user
              national_id:
                type: string
                description: national id
              national_id_type:
                type: string
                description: national id type
    """
    current_app.logger.info('Getting info from users')

    users = Users.query.all()
    users_list = []

    for user in users:
        user_object = {
            'id': user.id_user,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'alias': user.alias,
            'email': user.email,
            'national_id': user.national_id,
            'national_id_type': user.national_id_type
        }
        users_list.append(user_object)

    response_object = {
        'status': 'success',
        'data': {
            'users': users_list
        }
    }

    current_app.logger.info('Obtained info from users successfully.')
    return jsonify(response_object), 200
