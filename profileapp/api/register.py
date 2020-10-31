from profileapp import database
from profileapp.model import Users
from flask import request
from flask import Blueprint
from flask import jsonify
import json
from flask_expects_json import expects_json

schema_new_user = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'national_id': {'type': 'string'},
        'national_id_type': {'type': 'string'},
        'alias': {'type': 'string'},
        'password': {'type': 'string'},
        'profile': {'type': 'integer'}
    },
    'required': ['name', 'email', 'national_id', 'national_id_type', 'alias', 'password', 'profile']}

bp_register = Blueprint('register', __name__, url_prefix='/register/')


# TODO: CREATE USER TIENE Q TENER PERFIL/rol.. refactor para user y luego json register con profile

@bp_register.route("/", methods=['POST'])
@expects_json(schema_new_user)
def register_new_user():
    # @expects_json(schema_new_user)
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data
    post_data = request.get_json()

    user = Users(name=post_data['name'], email=post_data['email'],
                 national_id=post_data['national_id'], national_id_type=post_data['national_id_type'],
                 alias=post_data['alias'], password=post_data['password'])

    try:
        # add to the database session
        database.db.session.add(user)

        # commit to persist into the database
        database.db.session.commit()
    except:
        return jsonify({'error': "user already exist"})

    return jsonify({'id': user.id_user, 'name': user.name, 'alias': user.alias, 'email': user.email})
