from functools import wraps
from flask import request, abort


# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        print(request.headers)
        if request.headers.get('Token') and request.headers.get('Token') == 'dwight':
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function
