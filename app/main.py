from flask import Flask
from .routes import main
from .db import init_db

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # отключаем кэш статики

    init_db()

    app.register_blueprint(main)

    return app