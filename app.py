import os
import sys
from flask import Flask
from config import Config
from models import db
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    register_blueprints(app)

    with app.app_context():
        # Check if database exists; if not, create tables & seed dataset
        os.makedirs(os.path.dirname(Config.SQLITE_PATH), exist_ok=True)
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    print("Starting Retail Sales Analytics System Flask Web Server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
