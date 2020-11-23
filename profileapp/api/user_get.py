from flask import current_app
from flask import jsonify

from profileapp.Errors.ProfileAppException import ProfileAppException
from profileapp.api.utils import validate_user_id_exists
from profileapp.model import Users


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
