from profileapp import database
from profileapp.model import Users, Profile
from flask import request
from flask import Blueprint
from flask import jsonify
import hashlib
from flask_expects_json import expects_json

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
@expects_json(schema_new_user)
def login():
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

    return jsonify({'id': user.id_user, 'name': user.name, 'alias': user.alias, 'email': user.email}), 200


def user_exists(new_user_mail):
    if not Users.query.filter_by(email=new_user_mail).first() is None:
        return True
    return False


def user_password_empty(login_user_password):
    return login_user_password == ''


def correct_password(password_login, user_password):
    login_password = hashlib.md5(password_login.encode()).hexdigest()
    return user_password == login_password
