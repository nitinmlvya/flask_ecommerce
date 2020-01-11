from flask import Blueprint, jsonify, request, g
from flask import current_app as app
from itsdangerous import URLSafeSerializer
from flask_ecommerce import db, auth
from flask_ecommerce.users.models import User, UserDetails, Address

mod = Blueprint('users', __name__, url_prefix='/users')


@auth.verify_token
def verify_auth_token(token):
    print('----token', token)
    s = URLSafeSerializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except Exception:
        return False
    g.user = User.query.get(data['id'])
    return True

@mod.route('/', methods=['GET'])
@auth.login_required
def fetch_users():
    # users = User.query.with_entities(User.username, UserDetails.name).all()  # select * from user;
    # print(users), users[0].username)  # access using column name
    users = User.query.all()  # select * from user;
    # # Without representation
    # print(users[0].username)
    # print(users[0].email)
    # With represtation
    response = [user.to_representation() for user in users]
    return jsonify(response)


@mod.route('/get_user/<user_id>', methods=['GET'])
def fetch_user_by_id(user_id):
    users = User.query.get(int(user_id))
    response = users.to_representation()
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
    user = User.query.filter(User.username == username).first()
    # Sample query to execute on "OR" condition
    # user = User.query.filter((User.username == username) | (User.email == email)).first()
    response = user.to_representation()
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


@mod.route('/update_user/<user_id>', methods=['PUT'])
def update_user(user_id):
    request_data = request.get_json()
    user = User.query.get(int(user_id))
    user.email = request_data['email']
    db.session.commit()
    return 'User has been updated'


@mod.route('/add_user_detail', methods=['POST'])
def add_user_detail():
    request_data = request.get_json()
    user_detail = UserDetails(
        name=request_data['name'],
        user_id=request_data['user_id']
    )
    db.session.add(user_detail)
    db.session.commit()
    return 'User detail has been added.'


@mod.route('/fetch_user_detail', methods=['GET'])
def fetch_user_detail():
    user_details = UserDetails.query.all()
    response = [user_detail.to_representation() for user_detail in user_details]
    return jsonify(response)


@mod.route('/add_address', methods=['POST'])
def add_address():
    request_data = request.get_json()
    user_id = request_data['user_id']
    address = Address(
        city=request_data['city']
    )
    user = User.query.get(user_id)
    user.addresses.append(address)  # Add to association table
    # user.addressess.delete(address)  # delete from association table
    # db.session.add(address)
    db.session.commit()
    return 'Address detail has been added.'


@mod.route('/fetch_addressess', methods=['GET'])
def fetch_addressess():
    addresses = Address.query.all()
    response = [address.to_representation() for address in addresses]
    return jsonify(response)


@mod.route('/login', methods=['POST'])
def login():
    print('___login')
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    user = User.query.filter(User.username == username and User.password == password).first()
    token = user.generate_auth_token()
    reponse = token
    return jsonify(reponse)