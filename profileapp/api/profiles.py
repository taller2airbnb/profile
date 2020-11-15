from profileapp import database
from profileapp.model import Profile
from flask import request
from flask import Blueprint
from flask import jsonify
from flask_expects_json import expects_json
from flasgger.utils import swag_from
from flask import current_app


schema_new_user = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'description': {'type': 'string'}
    },
    'required': ['id', 'description']}

bp_profiles = Blueprint('profiles', __name__, url_prefix='/profiles/')


@bp_profiles.route("/add/", methods=['POST'])
@swag_from(methods=['POST'])
@expects_json(schema_new_user)
def add_new_profile():
    """
    Create a new profile
    Profile id and description is needed
    ---
    tags:
      - profiles
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
            required:
              - id
              - description
            properties:
              id:
                type: integer
                description: Unique identifier representing a profile description
              description:
                type: string
                description: representing a profile description
    responses:
      200:
        description: A successful profile creation
        schema:
          properties:
              id:
                type: integer
                description: Unique identifier representing a profile description
              description:
                type: string
                description: representing a profile description
    """
    # @expects_json(schema_new_user)
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data
    post_data = request.get_json()

    current_app.logger.info('Creating new profile: ' + post_data['description'])
    profile = Profile(id_profile=post_data['id'], description=post_data['description'])

    try:
        # add to the database session
        database.db.session.add(profile)

        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error('Profile creation failed: profile with id' + post_data['id'] + ' already exists.')
        return jsonify({'Error': "profile already exists"}), 400

    current_app.logger.info('Profile ' + post_data['description'] + ' successfully created.')
    return jsonify({'id': profile.id_profile, 'description': profile.description}), 200


@bp_profiles.route("/", methods=['GET'])
@swag_from(methods=['GET'])
def get_all_profiles():
    """
    Get all profiles
    Profile id and description is going to be given
    ---
    tags:
      - profiles
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: false
    responses:
      200:
        description: A list of profiles created
    """
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
