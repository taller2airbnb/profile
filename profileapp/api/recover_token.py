import secrets
from datetime import datetime
from threading import Thread

from flasgger.utils import swag_from
from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask_mail import Message, Mail

from profileapp import database
from profileapp.Errors.ProfileAppException import ProfileAppException
from profileapp.api.utils import validate_user_id_exists, get_email_from_user_id, validate_is_not_google_user_by_id, \
    validate_existent_user_by_mail, get_user_id_from_mail
from profileapp.model import RecoverUserToken

bp_recover_token = Blueprint('recover_token', __name__, url_prefix='/recover_token/')


@bp_recover_token.route("/<string:user_mail>", methods=['POST'])
@swag_from(methods=['POST'])
def generate_recover_token(user_mail):
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
        name: user_mail
        type: string
        required: true
    responses:
      200:
        description: A successful token recover creation
        schema:
          properties:
              mail:
                type: string
                description: Unique mail representing a profile description
              description:
                type: string
                description: representing a description
    """
    current_app.logger.info('Generating user token recover for user: ' + user_mail)

    try:
        validate_existent_user_by_mail(user_mail)
        user_id = get_user_id_from_mail(user_mail)
        validate_is_not_google_user_by_id(user_id)
        recipient = [user_mail]
        recover_user_token = generate_new_recover_user_token(user_id)

        commit_new_recover_user_token(recover_user_token, user_id)

        FlaskThread(target=send_async_email, args=(recipient, recover_user_token.recover_token)).start()

    except ProfileAppException as e:
        current_app.logger.error("Generation of token for user failed.")
        return jsonify({'Error': e.message}), e.error_code

    current_app.logger.info('Token for user ' + str(user_id) + ' successfully created.')
    return jsonify({'id': str(user_id), 'Description': 'Generated'}), 200


def send_async_email(recipient, token):
    with current_app.app_context():
        mail = Mail()
        msg = Message("Token for Bookbnb", recipients=recipient)
        msg.body = token
        mail.send(msg)


class FlaskThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()


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
