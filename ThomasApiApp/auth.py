from functools import wraps
from flask import request, abort

users = {  # TODO: Move to config file or some other secure method
    "user1": "password123"
}


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'POST':
            auth = request.authorization
            if not auth or not authenticate(auth.username, auth.password):
                abort(401)
        return f(*args, **kwargs)

    return decorated

def authenticate(username, password):
    if username in users and users[username] == password:
        return True
    return False