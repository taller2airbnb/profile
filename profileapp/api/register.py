from profileapp import database
from profileapp.model import Users, ProfileUser
from flask import request
from flask import Blueprint
from flask import jsonify
import hashlib
from flask_expects_json import expects_json
from profileapp.api.utils import validate_existent_profile_id, validate_free_user_identifiers, validate_user_password
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

bp_register = Blueprint('register', __name__, url_prefix='/register/')


@bp_register.route("/", methods=['POST'])
@swag_from(methods=['POST'])
@expects_json(schema_new_user)
def register_new_user():
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
        current_app.logger.error("Something happened creating the Profile-User relation for user " + post_data['email'] + "in the database.")
        return jsonify({'error': "Something happened creating the Profile-User relation in the Database"}), 400

    current_app.logger.info("Registration for user " + post_data['email'] + "succeeded.")
    return jsonify({'id': user.id_user, 'name': user.first_name, 'alias': user.alias, 'email': user.email}), 200
