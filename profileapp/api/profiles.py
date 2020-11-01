from profileapp import database
from profileapp.model import Profile
from flask import request
from flask import Blueprint
from flask import jsonify
from flask_expects_json import expects_json

schema_new_user = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'description': {'type': 'string'}
    },
    'required': ['id', 'description']}

bp_profiles = Blueprint('profiles', __name__, url_prefix='/profiles/')


@bp_profiles.route("/add/", methods=['POST'])
@expects_json(schema_new_user)
def add_new_profile():
    # @expects_json(schema_new_user)
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data
    post_data = request.get_json()

    profile = Profile(id_profile=post_data['id'], description=post_data['description'])

    try:
        # add to the database session
        database.db.session.add(profile)

        # commit to persist into the database
        database.db.session.commit()
    except:
        return jsonify({'error': "profile already exist"}), 400

    return jsonify({'id': profile.id_profile, 'description': profile.description}), 200


@bp_profiles.route("/", methods=['GET'])
def get_all_profiles():
    # Get all profiles
    profiles = Profile.query.all()
    profile_list = []
    for profile in profiles:
        profile_object = {
            'id': profile.id_profile,
            'description': profile.description
        }
        profile_list.append(profile_object)
    response_object = {
        'status': 'success',
        'data': {
            'profiles': profile_list
        }
    }
    return jsonify(response_object), 200