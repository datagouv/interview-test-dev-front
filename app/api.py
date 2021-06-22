
from werkzeug.wrappers import Response
from flask import Blueprint, request, g, jsonify
from marshmallow import Schema, fields, ValidationError, post_load

import random
import string
from app import db
from app.models import User, BlacklistToken
from app.decorators import login_required
from app.utils import hash_str


bp = Blueprint('api', __name__)


class UserSchema(Schema):
    username = fields.Str(required=True)
    registered_on = fields.DateTime(dump_only=True)
    password = fields.Str(required=True, load_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class HashSchema(Schema):
    string = fields.Str(required=True)
    algorithm = fields.Str(required=True)


@bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json() or {}

    try:
        new_user = UserSchema().load(data)
    except ValidationError as err:
        resp = jsonify({'message': err.messages})
        resp.status_code = 400
        return resp

    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({'message': 'this username already exists'}), 409

    try:
        db.session.add(new_user)
        db.session.commit()

        auth_token = new_user.encode_auth_token(new_user.id)
        return jsonify({'token': auth_token}), 201
    except Exception as err:
        resp = jsonify({'message': str(err)})
        resp.status_code = 500
        return resp


@bp.route('/login', methods=['POST'])
def login_user() -> Response:
    data = request.get_json() or {}

    try:
        valid_data = LoginSchema().load(data)
    except ValidationError as err:
        resp = jsonify({'message': err.messages})
        resp.status_code = 400
        return resp

    try:
        user = User.query.filter_by(username=valid_data['username']).first()
        if user and user.check_password(valid_data['password']):
            auth_token = user.encode_auth_token(user.id)
            return jsonify({'token': auth_token}), 201
        else:
            resp = jsonify({'message': 'Bad credentials'})
            resp.status_code = 401
            return resp
    except Exception as err:
        resp = jsonify({'message': str(err)})
        resp.status_code = 500
        return resp


@bp.route('/logout', methods=['POST'])
@login_required
def logout_user():
    auth_token = g.current_auth_token
    blacklist_token = BlacklistToken(token=auth_token)
    try:
        db.session.add(blacklist_token)
        db.session.commit()
        return jsonify({'message': 'Successfully logged out.'}), 200
    except Exception as err:
        resp = jsonify({'message': str(err)})
        resp.status_code = 500
        return resp


@bp.route('/dummy-hash', methods=['GET'])
def calculate_dummy_hash():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(20))

    hash = hash_str(random_string, 'sha256')

    return jsonify({'random_string': random_string, 'random_hash': hash}), 200


@bp.route('/hash', methods=['POST'])
def calculate_hash():
    data = request.get_json() or {}

    try:
        valid_data = HashSchema().load(data)
    except ValidationError as err:
        resp = jsonify({'message': err.messages})
        resp.status_code = 400
        return resp

    if valid_data['algorithm'] not in ['md5', 'sha1', 'sha256']:
        resp = jsonify({'message': 'unsupported algorithm'})
        resp.status_code = 400
        return resp

    hash = hash_str(valid_data['string'], valid_data['algorithm'])

    return jsonify({'hash': hash}), 200
