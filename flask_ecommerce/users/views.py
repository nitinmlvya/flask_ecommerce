from flask import Blueprint, jsonify, request

from flask_ecommerce import db
from flask_ecommerce.users.models import User

mod = Blueprint('users', __name__, url_prefix='/users')

@mod.route('/', methods=['GET'])
def fetch_users():
    users = User.query.all()
    response = [user.__repr__() for user in users]
    return jsonify(response)

@mod.route('/get_user/<user_id>', methods=['GET'])
def fetch_user_by_id(user_id):
    users = User.query.get(int(user_id))
    response = users.__repr__()
    response.pop('password')
    """
    #Execute query using raw sql query
    result = db.engine.execute('SELECT * FROM user where id = {}'.format(int(user_id)))
    for row in result:
        response = {
            'username': row['username'],
            'email': row['email']
        }
        break
    """
    return jsonify(response)

@mod.route('/get_user', methods=['GET'])
def fetch_user_by_username():
    username = request.args.get('username')
    user = User.query.filter(User.username==username).first()
    # Sample query to execute on "OR" condition
    # user = User.query.filter((User.username == username) | (User.email == email)).first()
    response = user.__repr__()
    return jsonify(response)

@mod.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(int(user_id))
    db.session.delete(user)
    db.session.commit()
    return 'User has been deleted.'


@mod.route('/create_user', methods=['POST'])
def create_user():
    request_data = request.get_json()
    user = User(
        username=request_data['username'],
        email=request_data['email'],
        password=request_data['password'],
    )
    db.session.add(user)
    db.session.commit()
    return 'User has been created'