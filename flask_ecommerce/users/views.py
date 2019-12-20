import json

from flask import Blueprint, jsonify

mod = Blueprint('users', __name__, url_prefix='/users')

data = json.load(open('data.json'))

@mod.route('/', methods=['GET'])
def fetchall():
    """
    Fetch all the users
    :return: List of the users.
    """
    return jsonify(data)

@mod.route('/<user_id>', methods=['GET'])
def fetch_one(user_id):
    """
    Fetch single user details
    :param user_id: User ID
    :return: Detail of the user
    """
    user_detail = [x for x in data if x['id'] == int(user_id)]
    user_detail = user_detail[0] if user_detail else {}
    return jsonify(user_detail)