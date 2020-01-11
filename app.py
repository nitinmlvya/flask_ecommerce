import os
from flask_ecommerce import create_app, db

config_name = os.getenv('FLASK_CONFIG', 'development') # Default is 'development' if FLASK_CONFIG is not set.
app = create_app(config_name)

if __name__=='__main__':
    with app.app_context(): # Allow application context
        db.create_all() # Create tables only.
    app.run()