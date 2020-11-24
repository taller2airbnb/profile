import secrets
from datetime import datetime

from flasgger.utils import swag_from
from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask_mail import Message, Mail

from profileapp import database
from profileapp.Errors.ProfileAppException import ProfileAppException
from profileapp.api.utils import validate_user_id_exists, get_email_from_user_id, validate_is_not_google_user_by_id
from profileapp.model import RecoverUserToken

bp_recover_token = Blueprint('recover_token', __name__, url_prefix='/recover_token/')


@bp_recover_token.route("/<int:user_id>", methods=['POST'])
@swag_from(methods=['POST'])
def generate_recover_token(user_id):
    """
    Create a new profile
    Profile id and description is needed
    ---
    tags:
      - recover_token
    consumes:
      - application/json
    parameters:
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      200:
        description: A successful token recover creation
        schema:
          properties:
              id:
                type: integer
                description: Unique identifier representing a profile description
              description:
                type: string
                description: representing a description
    """
    current_app.logger.info('Generating user token recover for user: ' + str(user_id))

    try:
        validate_user_id_exists(user_id)
        validate_is_not_google_user_by_id(user_id)
        recipient = [get_email_from_user_id(user_id)]
        recover_user_token = generate_new_recover_user_token(user_id)

        commit_new_recover_user_token(recover_user_token, user_id)

        with current_app.app_context():
            mail = Mail()
            msg = Message("Token for Bookbnb", recipients=recipient)
            msg.body = recover_user_token.recover_token
            mail.send(msg)

    except ProfileAppException as e:
        current_app.logger.error("Generation of token for user failed.")
        return jsonify({'Error': e.message}), e.error_code

    current_app.logger.info('Token for user ' + str(user_id) + ' successfully created.')
    return jsonify({'id': str(user_id), 'Description': 'Generated'}), 200


def generate_new_recover_user_token(user_id):
    recover_user_token = RecoverUserToken.query.filter_by(id_user=user_id).first()
    token = str(secrets.token_urlsafe(16))

    if recover_user_token is None:
        recover_user_token = RecoverUserToken(id_user=user_id, recover_token=token)
    else:
        recover_user_token.recover_token = token
        recover_user_token.date_created = datetime.now()

    return recover_user_token


def commit_new_recover_user_token(recover_user_token, user_id):
    try:
        # add to the database session
        database.db.session.add(recover_user_token)

        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error("Something happened creating the token for user: " + str(user_id))
        return jsonify({'Error': "Something happened creating the token in the Database"}), 400
