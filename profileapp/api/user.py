from flasgger.utils import swag_from
from flask import Blueprint
from flask_expects_json import expects_json

from profileapp.api.api_validator import require_appkey
from profileapp.api.user_get import get_fields_from_users, get_fields_from_user
from profileapp.api.user_post import register_new_user, schema_new_user
from profileapp.api.user_put import modify_user, schema_modify_user, blocked_status, new_password, add_push_token

bp_user = Blueprint('user', __name__, url_prefix='/user/')


@bp_user.route("/", methods=['POST'])
@require_appkey
@swag_from(methods=['POST'])
@expects_json(schema_new_user)
def register_new_user_api():
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
    security:
      - APIKeyHeader: ['Token']
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
    return register_new_user()


@bp_user.route("/", methods=['PUT'])
@require_appkey
@swag_from(methods=['PUT'])
@expects_json(schema_modify_user)
def modify_user_api():
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
    security:
      - APIKeyHeader: ['Token']
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
    return modify_user()


@bp_user.route("/<int:user_id>/blocked_status/", methods=['PUT'])
@require_appkey
@swag_from(methods=['PUT'])
def blocked_status_api(user_id):
    """
    Change Blocked status for user's by id
    ---
    tags:
      - user
    consumes:
      - application/json
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
            required:
              - new_status
            properties:
              new_status:
                type: boolean
                description: New blocked status.
    security:
      - APIKeyHeader: ['Token']
    responses:
      200:
        description: A successful change of user blocked status.
        schema:
          properties:
              user_id:
                type: integer
                description: Unique identifier representing the user.
              block_user:
                type: string
                description: Expected 'Blocked'.
    """
    return blocked_status(user_id)


@bp_user.route("/<string:user_mail>/password/", methods=['PUT'])
@require_appkey
@swag_from(methods=['PUT'])
def new_password_api(user_mail):
    """
    Change Password for user's by id and token
    ---
    tags:
      - user
    consumes:
      - application/json
    parameters:
      - in: path
        name: user_mail
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
            required:
              - token
              - new_password
            properties:
              token:
                type: string
                description: Token for validate new password.
              new_password:
                type: string
                description: New password.
    security:
      - APIKeyHeader: ['Token']
    responses:
      200:
        description: A successful change of user blocked status.
        schema:
          properties:
              user_mail:
                type: string
                description: Unique mail representing the user.
              block_user:
                type: string
                description: Expected 'Blocked'.
    """
    return new_password(user_mail)


@bp_user.route("/<int:id>", methods=['GET'])
@require_appkey
@swag_from(methods=['GET'])
def get_fields_from_user_api(id):
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
    security:
      - APIKeyHeader: ['Token']
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
    return get_fields_from_user(id)


@bp_user.route("/", methods=['GET'])
@require_appkey
@swag_from(methods=['GET'])
def get_fields_from_users_api():
    """
    Get fields from user
    Profile id and description is going to be given
    ---
    tags:
      - user
    security:
      - APIKeyHeader: ['Token']
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
    return get_fields_from_users()


@bp_user.route("/<int:user_id>/push_token/", methods=['PUT'])
@require_appkey
@swag_from(methods=['PUT'])
def add_push_token_api(user_id):
    """
    Change Push Token for user's by id
    ---
    tags:
      - user
    consumes:
      - application/json
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
            required:
              - push_token
            properties:
              push_token:
                type: string
                description: New push token.
    security:
      - APIKeyHeader: ['Token']
    responses:
      200:
        description: A successful change of user blocked status.
        schema:
          properties:
              user_id:
                type: integer
                description: Unique identifier representing the user.
              push_token:
                type: string
                description: token
    """
    return add_push_token(user_id)
