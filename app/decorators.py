from functools import wraps
from flask import request, g, jsonify

from app.models import User


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('authorization', None)
        if auth_header is None:
            resp = jsonify({'message': 'Provide a valid auth token.'})
            resp.status_code = 403
            return resp

        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            resp = jsonify({'message': 'Bearer token malformed.'})
            resp.status_code = 403
            return resp

        resp = User.decode_auth_token(auth_token)

        if isinstance(resp, str):
            resp = jsonify({'message': resp})
            resp.status_code = 401
            return resp

        user = User.query.filter_by(id=resp).first()
        if not user:
            resp = jsonify({'message': 'Bad credentials'})
            resp.status_code = 401
            return resp
        g.user = user
        g.current_auth_token = auth_token

        return f(*args, **kwargs)
    return decorated_function
