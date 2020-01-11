import json
from flask import Blueprint, jsonify, request

mod = Blueprint('json_users', __name__, url_prefix='/json_users')

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
    Permalink URL format 1
    Fetch single user details
    :param user_id: User ID
    :return: Detail of the user
    """
    user_detail = [x for x in data if x['id'] == int(user_id)]
    user_detail = user_detail[0] if user_detail else {}
    return jsonify(user_detail)

@mod.route('/get_user/', methods=['GET'])
def fetch_one_permalink_default():
    """
    Permalink URL format 2 = Default
    Fetch single user details
    :return: Detail of the user
    """
    user_id = request.args.get('user_id')
    user_detail = [x for x in data if x['id'] == int(user_id)]
    user_detail = user_detail[0] if user_detail else {}
    return jsonify(user_detail)

@mod.route('/create_user_json_req', methods=['POST'])
def create_user_using_json_request():
    """
    Create a user
    """
    request_data = request.get_json() # It is mutable
    new_user_id = data[-1]['id'] + 1
    request_data['id'] = new_user_id
    data.append(request_data)
    json.dump(data, open('data.json', 'w'))
    response = request_data
    return jsonify(response)

@mod.route('/create_user_form_req', methods=['POST'])
def create_user_using_form_request():
    """
    Create a user
    """
    # request.form is immutable. To make mutable convert it to dictionary
    print('request_data:', request.form.to_dict())
    username = request.form.get('username')
    password = request.form.get('password')
    new_user_id = data[-1]['id'] + 1
    response = {
        'id': new_user_id,
        'username': username,
        'password': password
    }
    data.append(response)
    json.dump(data, open('data.json', 'w'))
    return jsonify(response)

@mod.route('/update_user/<user_id>/', methods=['PUT'])
def update_user(user_id):
    """
    Update the user information
    :return: Updated user information
    """
    request_data = request.get_json()
    print('request_data: ', request_data)
    for d in data:
        if d['id'] == int(user_id):
            if 'username' in request_data:
                d['username'] = request_data['username']
            if 'password' in request_data:
                d['password'] = request_data['password']
    json.dump(data, open('data.json', 'w'))
    return "User details updated."

@mod.route('/delete_user/<user_id>/', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete the user information
    """
    for index, d in enumerate(data):
        if d['id'] == int(user_id):
            del data[index]
    json.dump(data, open('data.json', 'w'))
    return "User has been deleted."