"""
https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
"backref" is a simple way to also declare a new property on the Address class.
You can then also use my_address.person to get to the person at that address.

"lazy" defines when SQLAlchemy will load the data from the database:
"select" (which is the default) means that SQLAlchemy will load the data as necessary in one go
using a standard select statement.
"joined" tells SQLAlchemy to load the relationship in the same query as the parent using a JOIN statement.
"subquery" works like 'joined' but instead, SQLAlchemy will use a subquery.
"dynamic" is special and useful if you have many items. Instead of loading the items SQLAlchemy will
return another query object which you can further refine before loading the items.
This is usually what you want if you expect more than a handful of items for this relationship.

"Custom Join query:"
User.query.join(
            Address, (User.id == Address.user.id)).filter(<condition>) OR all()
"""
from itsdangerous import URLSafeSerializer

from flask_ecommerce import db, auth
from flask import current_app as app, g

users_addresses = db.Table('users_addresses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('address_id', db.Integer, db.ForeignKey('address.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement = True)
    username = db.Column('username', db.String(64), index=True, unique=True)
    email = db.Column('email', db.String(120), unique=True)
    password = db.Column('password', db.String(128))
    user_detail = db.relationship('UserDetails', backref='user', lazy=True, uselist=False, cascade="all,delete",
                                  ) # one-to-one relationship
    addresses = db.relationship('Address', secondary=users_addresses, backref='user', lazy='joined' #use 'dynamic' and check the difference
                                , cascade="all,delete"
                                 ) # Many-to-many Relationship

    def to_representation(self):
        if self.user_detail:
            user_detail = self.user_detail.to_representation()
        else:
            user_detail = {}
        addresses = [x.to_representation() for x in self.addresses]
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'user_detail': user_detail,
            'addresses': addresses
        }

    def generate_auth_token(self):
        s = URLSafeSerializer(app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})


class UserDetails(db.Model):
    __tablename__ = 'user_details'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement = True)
    name = db.Column('name', db.String(64), nullable=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_representation(self):
        return {
            'name': self.name
        }

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement = True)
    city = db.Column('city', db.String(64), nullable=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_representation(self):
        return {
            'city': self.city
        }