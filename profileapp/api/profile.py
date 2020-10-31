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

bp_profile = Blueprint('profile', __name__, url_prefix='/profile/')


@bp_profile.route("/add/", methods=['POST'])
@expects_json(schema_new_user)
def register_new_user():
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

    return jsonify({'id': profile.id_profile, 'descrip': profile.description}), 200
