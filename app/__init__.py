from flask import Flask
from .routes import deck_blueprint
from .utils import preload_all_cached_data

def create_app():
    preload_all_cached_data()
    app = Flask(__name__)
    app.register_blueprint(deck_blueprint)
    return app