from flask_ecommerce import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))


    def __repr__(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }