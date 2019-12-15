from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import a module / component using its blueprint handler variable
    from flask_ecommerce.users.views import mod as users_module

    # Register blueprint(s)
    app.register_blueprint(users_module)
    return app