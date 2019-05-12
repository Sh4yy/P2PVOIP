from flask import Blueprint, jsonify, request, abort, g
from models import User
import functools


mod = Blueprint(__name__, 'routes')


def contains(json, keys):
    if not all([key in json for key in keys]):
        raise abort(401)


def error(reason):
    return jsonify({'ok': False,
                    'msg': reason})


def authorized(func):

    @functools.wraps(func)
    def inner(*args, **kwargs):
        head = request.headers.get('Authorization')
        if not head:
            return abort(401)

        method, token = head.split()
        if not token or not method:
            return abort(401)

        if method != 'Bearer':
            return abort(401)

        user = User.select().where(User.auth_token == token).get()
        if not user:
            return abort(401)

        g.user = user
        return func(*args, **kwargs)

    return inner


@mod.route('/login', methods=['POST'])
def login():
    """
    requires Username, Password
    :return:
    """

    pswd = request.authorization.password
    username = request.authorization.username

    try:
        token = User.login(username, pswd)
    except Exception as e:
        return error(str(e))

    return jsonify({
        'ok': True,
        'token': token
    })


@mod.route('/register', methods=['POST'])
def register():
    """
    register new user
    :return:
    """

    pswd = request.authorization.password
    username = request.authorization.username
    user = User.register(username, pswd)

    return jsonify({
        "ok": True,
        "username": user.username
    })


@mod.route('/user/<username>/address', methods=['GET'])
@authorized
def get_user_address(username):

    user = User.find(username)
    if not user:
        raise abort(404)

    if not user.get_address():
        return error("address is not available")

    return jsonify({
        "ok": True,
        "address": user.get_address()
    })


@mod.route('/user/me/address', methods=['POST'])
@authorized
def set_address():

    user = g.user
    print(request.json)
    user.set_ip(request.json.get('address'))

    return jsonify({
        "ok": True,
        "address": user.get_address()
    })