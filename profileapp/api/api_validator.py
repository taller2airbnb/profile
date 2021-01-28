from profileapp.Errors.ProfileAppException import ProfileAppException
from functools import wraps
from flask import request, abort, current_app, jsonify

from profileapp.Errors import APIKeyError
from profileapp.model import APIKeyToken


def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if current_app.config['TESTING']:
            return view_function(*args, **kwargs)
        try:
            token = validate_existent_token(request.headers)
            if request.headers.get('Token') and request.headers.get('Token') == token:
                return view_function(*args, **kwargs)
            else:
                abort(401)
        except ProfileAppException as e:
            current_app.logger.error("Registration with API KEY Token failed.")
            return jsonify({'Error': e.message}), e.error_code

    return decorated_function


def validate_existent_token(header):
    if request.headers.get('Token'):
        token = request.headers.get('Token')
    else:
        raise APIKeyError.APIKeyNotExistent('')
    mail_taken = APIKeyToken.query.filter_by(api_key_token=token).first()
    if mail_taken is None:
        raise APIKeyError.APIKeyNotExistent(token)
    if not mail_taken.active:
        raise APIKeyError.APIKeyNotExistent(token)
    return mail_taken.api_key_token

