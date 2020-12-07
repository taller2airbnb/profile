import hashlib

from flask import current_app
from flask import jsonify
from flask import request

from profileapp import database
from profileapp.Errors.ProfileAppException import ProfileAppException
from profileapp.api.utils import validate_user_id_exists, validate_modify_schema_not_empty, validate_user_password, \
    validate_password_recovery
from profileapp.model import Users

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


def modify_user():
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


def blocked_status(user_id):
    new_status = (request.get_json())['new_status']
    current_app.logger.info('Blocking user: ' + str(user_id))
    try:
        validate_user_id_exists(user_id)
    except ProfileAppException as e:
        current_app.logger.error("Block user " + str(user_id) + " failed.")
        return jsonify({'Error': e.message}), e.error_code

    user = Users.query.filter_by(id_user=user_id).first()

    user.blocked = new_status

    try:
        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error("Error when attempting to block user " + str(user_id) + " in the database.")
        return jsonify({'Error': "Something happened when attempting to block user in the Database"}), 400

    current_app.logger.info("Blocking for user with id " + str(user_id) + " succeeded.")
    return jsonify({'id': user.id_user, 'modify_user': 'OK'}), 200


def new_password(user_id):
    user_new_password_plain = (request.get_json())['new_password']
    user_new_password = hashlib.md5(user_new_password_plain.encode()).hexdigest()

    token = (request.get_json())['token']

    current_app.logger.info('Initializing password recovery for user: ' + str(user_id))
    try:
        validate_user_password(user_new_password)
        validate_user_id_exists(user_id)
        validate_password_recovery(user_id, token)
    except ProfileAppException as e:
        current_app.logger.error("Block user " + str(user_id) + " failed.")
        return jsonify({'Error': e.message}), e.error_code

    user = Users.query.filter_by(id_user=user_id).first()

    try:
        user.password = user_new_password
        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error("Error when attempting to change password of  user " + str(user_id) + " in the database.")
        return jsonify({'Error': "Something happened when attempting to change password of user in the Database"}), 400

    current_app.logger.info("Password change for user with id " + str(user_id) + " succeeded.")
    return jsonify({'id': user.id_user, 'modify_user': 'OK'}), 200


