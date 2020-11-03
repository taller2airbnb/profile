from flask import request, Blueprint, jsonify
from flask_expects_json import expects_json
from profileapp.api.register import schema_new_user, register_new_user
from profileapp.api.utils import profile_exists, profile_is_admin


bp_register_admin = Blueprint('register_admin', __name__, url_prefix='/register_admin/')


@bp_register_admin.route("/", methods=['POST'])
@expects_json(schema_new_user)
def register_new_admin():

    # @expects_json(schema_new_user), just like register
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data
    post_data = request.get_json()

    if not profile_exists(post_data['profile']):
        return jsonify({'error': "non existent profile"}), 400

    if not profile_is_admin(post_data['profile']):
        return jsonify({'error': "profile is not admin"}), 400

    return register_new_user()
