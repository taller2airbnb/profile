from flask import current_app
from flask import jsonify

from profileapp.Errors.ProfileAppException import ProfileAppException
from profileapp.api.utils import validate_user_id_exists
from profileapp.model import Users


def get_fields_from_user(id):
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
        'national_id_type': user.national_id_type,
        'blocked': user.blocked
    }
    current_app.logger.info('Obtained info from user: ' + str(id) + ' successfully.')
    return jsonify(response_object), 200


def get_fields_from_users():
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
            'national_id_type': user.national_id_type,
            'blocked': user.blocked
        }
        users_list.append(user_object)

    response_object = {
            'users': users_list
    }

    current_app.logger.info('Obtained info from users successfully.')
    return jsonify(response_object), 200
