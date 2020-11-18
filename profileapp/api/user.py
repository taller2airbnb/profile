import hashlib

from profileapp import database
from profileapp.model import Users, ProfileUser
from flask import request
from flask import Blueprint
from flask import jsonify
from flask_expects_json import expects_json
from profileapp.api.utils import validate_user_id_exists, validate_modify_schema_not_empty, \
    validate_existent_profile_id, validate_free_user_identifiers, validate_user_password
from flasgger.utils import swag_from
from profileapp.Errors.ProfileAppException import ProfileAppException
from flask import current_app

schema_new_user = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string'},
        'national_id': {'type': 'string'},
        'national_id_type': {'type': 'string'},
        'alias': {'type': 'string'},
        'password': {'type': 'string'},
        'profile': {'type': 'integer'}
    },
    'required': ['first_name', 'last_name', 'email', 'national_id', 'national_id_type', 'alias', 'password', 'profile']}

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

schema_get_user_by_id = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'}
    },
    'required': ['id']
}

bp_user = Blueprint('user', __name__, url_prefix='/user/')


@bp_user.route("/", methods=['POST'])
@swag_from(methods=['POST'])
@expects_json(schema_new_user)
def register_new_user():
    """
    Register a new user
    The new user has to fulfill all the required fields
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
              - first_name
              - last_name
              - email
              - national_id
              - national_id_type
              - alias
              - password
              - profile
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
              profile:
                type: integer
                description: Profile of the new user, has to be an existing one (check /profiles/)
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
    current_app.logger.info("Registering user " + post_data['email'])
    try:
        validate_existent_profile_id(post_data['profile'])
        validate_free_user_identifiers(post_data['email'], post_data['alias'])
        validate_user_password(post_data['password'])
    except ProfileAppException as e:
        current_app.logger.error("Registration for user " + post_data['email'] + "failed.")
        return jsonify({'Error': e.message}), 400

    password = hashlib.md5(post_data['password'].encode()).hexdigest()

    user = Users(first_name=post_data['first_name'], last_name=post_data['last_name'], email=post_data['email'],
                 national_id=post_data['national_id'], national_id_type=post_data['national_id_type'],
                 alias=post_data['alias'], password=password)

    try:
        # add to the database session
        database.db.session.add(user)

        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error("Something happened creating the user " + post_data['email'] + "in the database.")
        return jsonify({'Error': "Something happened creating the User in the Database"}), 400

    user_created = Users.query.filter_by(email=post_data['email']).first()
    profile_user = ProfileUser(id_user=user_created.id_user, id_profile=post_data['profile'])

    try:
        # add to the database session
        database.db.session.add(profile_user)

        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error(
            "Something happened creating the Profile-User relation for user " + post_data['email'] + "in the database.")
        return jsonify({'error': "Something happened creating the Profile-User relation in the Database"}), 400

    current_app.logger.info("Registration for user " + post_data['email'] + "succeeded.")
    return jsonify({'id': user.id_user, 'name': user.first_name, 'alias': user.alias, 'email': user.email}), 200


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
        return jsonify({'Error': e.message}), 400

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


@bp_user.route("/<id>", methods=['GET'])
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
        required: true
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
    current_app.logger.info('Getting info from user: ' + id)
    try:
        validate_user_id_exists(id)
    except ProfileAppException as e:
        current_app.logger.error("Getting info from user " + id + " failed.")
        return jsonify({'Error': e.message}), 400

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
    current_app.logger.info('Obtained info from user: ' + id + ' successfully.')
    return jsonify(response_object), 200
