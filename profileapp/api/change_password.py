from profileapp import database
from profileapp.model import Users, Profile, ProfileUser
from flask import request
from flask import Blueprint
from flask import jsonify
import hashlib
from flask_expects_json import expects_json

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
@expects_json(schema_change_pass)
def change_password():
    post_data = request.get_json()

    if post_data['validate'] != 'OK':
        return jsonify({'error': "change password request not valid"}), 400

    if user_password_empty(post_data['new_pass']):
        return jsonify({'error': "password is empty"}), 400

    if not user_exists(post_data['email']):
        return jsonify({'error': "user not existent"}), 400

    new_password = hashlib.md5(post_data['new_pass'].encode()).hexdigest()
    user = Users.query.filter_by(email=post_data['email']).first()

    try:
        # change password
        user.password = new_password

        # commit to persist into the database
        database.db.session.commit()
    except:
        return jsonify({'error': "error"}), 400

    return jsonify({'email': user.email, 'change_pass': 'OK'}), 200


def user_password_empty(new_user_password):
    return new_user_password == ''


def user_exists(new_user_mail):
    if not Users.query.filter_by(email=new_user_mail).first() is None:
        return True
    return False
