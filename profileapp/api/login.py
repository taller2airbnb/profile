from profileapp import database
from profileapp.model import Users, ProfileUser
from flask import request
from flask import Blueprint
from flask import jsonify
from flask_expects_json import expects_json
from profileapp.api.utils import user_password_empty, user_exists, correct_password
from flasgger.utils import swag_from

schema_new_user = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string'},
        'alias': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['email', 'password']}

bp_login = Blueprint('login', __name__, url_prefix='/login/')


@bp_login.route("/", methods=['POST'])
@swag_from(methods=['POST'])
@expects_json(schema_new_user)
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
              - email
              - password
            properties:
              email:
                type: string
                description: Unique identifier representing a existent user
              password:
                type: string
                description: password of the user
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

    if user_password_empty(post_data['password']):
        return jsonify({'error': "password is empty"}), 400

    if not user_exists(post_data['email']):
        return jsonify({'error': "user not existent"}), 400

    user = Users.query.filter_by(email=post_data['email']).first()

    if not correct_password(post_data['password'], user.password):
        return jsonify({'error': "login failed"}), 400

    profile_user = ProfileUser.query.filter_by(id_user=user.id_user).first()

    return jsonify({'id': user.id_user, 'name': user.first_name, 'alias': user.alias, 'email': user.email,
                    'profile': profile_user.id_profile}), 200
