from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config

# db variable initialization
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    # Import a module / component using its blueprint handler variable
    from flask_ecommerce.users.views_json import mod as json_users_module
    from flask_ecommerce.users.views import mod as users_module

    # Register blueprint(s)
    app.register_blueprint(json_users_module)
    app.register_blueprint(users_module)
    return app