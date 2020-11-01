from profileapp import database
from profileapp.model import Users, Profile, ProfileUser
from flask import request
from flask import Blueprint
from flask import jsonify
import hashlib
from flask_expects_json import expects_json

schema_new_user = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string'},
        'national_id': {'type': 'string'},
        'national_id_type': {'type': 'string'},
        'alias': {'type': 'string'},
        'password': {'type': 'string'},
        'profile': {'type': 'integer'}
    },
    'required': ['first_name', 'last_name', 'email', 'national_id', 'national_id_type', 'alias', 'password', 'profile']}

bp_register = Blueprint('register', __name__, url_prefix='/register/')


@bp_register.route("/", methods=['POST'])
@expects_json(schema_new_user)
def register_new_user():
    # @expects_json(schema_new_user)
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data
    post_data = request.get_json()

    if not profile_exists(post_data['profile']):
        return jsonify({'error': "non existent profile"}), 400

    if user_exists(post_data['email'], post_data['alias']):
        return jsonify({'error': "user already exists"}), 400

    if user_password_empty(post_data['password']):
        return jsonify({'error': "password is empty"}), 400

    password = hashlib.md5(post_data['password'].encode()).hexdigest()

    user = Users(first_name=post_data['first_name'], last_name=post_data['last_name'], email=post_data['email'],
                 national_id=post_data['national_id'], national_id_type=post_data['national_id_type'],
                 alias=post_data['alias'], password=password)

    try:
        # add to the database session
        database.db.session.add(user)

        # commit to persist into the database
        database.db.session.commit()
    except:
        return jsonify({'error': "error"}), 400

    user_created = Users.query.filter_by(email=post_data['email']).first()
    profile_user = ProfileUser(id_user=user_created.id_user,id_profile=post_data['profile'])

    try:
        # add to the database session
        database.db.session.add(profile_user)

        # commit to persist into the database
        database.db.session.commit()
    except:
        return jsonify({'error': "error"}), 400

    return jsonify({'id': user.id_user, 'name': user.first_name, 'alias': user.alias, 'email': user.email}), 200


def profile_exists(new_user_profile):
    return Profile.query.filter_by(id_profile=new_user_profile).first() is not None


def user_exists(new_user_mail, new_user_alias):
    if not Users.query.filter_by(email=new_user_mail).first() is None:
        return True
    if not Users.query.filter_by(alias=new_user_alias).first() is None:
        return True
    return False


def user_password_empty(new_user_password):
    return new_user_password == ''
