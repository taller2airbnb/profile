from profileapp import database
from profileapp.model import Users, Profile, ProfileUser
from flask import request
from flask import Blueprint
from flask import jsonify
import hashlib
from flask_expects_json import expects_json
from flasgger.utils import swag_from
from profileapp.api.utils import validate_user_password, validate_existent_user_by_mail
from profileapp.Errors.ProfileAppException import ProfileAppException
from flask import current_app

schema_change_pass = {
    'type': 'object',
    'properties': {
        'validate': {'type': 'string'},
        'email': {'type': 'string'},
        'new_pass': {'type': 'string'}
    },
    'required': ['validate', 'email', 'new_pass']}

bp_change_password = Blueprint('change_password', __name__, url_prefix='/change_password/')


@bp_change_password.route("/", methods=['POST'])
@swag_from(methods=['POST'])
@expects_json(schema_change_pass)
def change_password():
    """
    Change Password
    Existent user is needed
    ---
    tags:
      - change-password
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
            required:
              - validate
              - email
              - password
            properties:
              validate:
                type: string
                description: Must Be "OK"
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
    """
    post_data = request.get_json()
    current_app.logger.info("Attempting password change for " + post_data['email'])

    if post_data['validate'] != 'OK':
        current_app.logger.error("Change password request for " + post_data['email'] + " is not valid.")
        return jsonify({'error': "change password request not valid"}), 400

    try:
        validate_existent_user_by_mail(post_data['email'])
        validate_user_password(post_data['new_pass'])
    except ProfileAppException as e:
        current_app.logger.error("Password change for " + post_data['email'] + " failed.")
        return jsonify({'Error': e.message}), 400

    new_password = hashlib.md5(post_data['new_pass'].encode()).hexdigest()
    user = Users.query.filter_by(email=post_data['email']).first()

    try:
        # change password
        user.password = new_password

        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error("Something happened when attempting password change for " + post_data['email'] + " in the database.")
        return jsonify({'Error': "Something happened changing the Password in the Database"}), 400

    current_app.logger.info("Password change for " + post_data['email'] + " succeeded.")
    return jsonify({'email': user.email, 'change_pass': 'OK'}), 200
