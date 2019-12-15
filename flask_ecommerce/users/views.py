from flask import Blueprint, jsonify

mod = Blueprint('users', __name__, url_prefix='/users')

@mod.route('/', methods=['GET'])
def fetchall():
    return 'List of users.'

@mod.route('/<user_id>', methods=['GET'])
def show(user_id):
    print(user_id)
    return jsonify({})