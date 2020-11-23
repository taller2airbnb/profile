from flasgger.utils import swag_from
from flask import Blueprint
from flask_expects_json import expects_json

from profileapp.api.user_get import get_fields_from_users, get_fields_from_user
from profileapp.api.user_post import register_new_user, schema_new_user
from profileapp.api.user_put import modify_user, schema_modify_user

bp_user = Blueprint('user', __name__, url_prefix='/user/')


@bp_user.route("/", methods=['POST'])
@swag_from(methods=['POST'])
@expects_json(schema_new_user)
def register_new_user_api():
    return register_new_user()


@bp_user.route("/", methods=['PUT'])
@swag_from(methods=['PUT'])
@expects_json(schema_modify_user)
def modify_user_api():
    return modify_user()


@bp_user.route("/<int:id>", methods=['GET'])
@swag_from(methods=['GET'])
def get_fields_from_user_api(id):
    return get_fields_from_user(id)


@bp_user.route("/", methods=['GET'])
@swag_from(methods=['GET'])
def get_fields_from_users_api():
    return get_fields_from_users()
