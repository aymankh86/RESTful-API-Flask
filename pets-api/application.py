import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from subprocess import call
from flask import Flask
from flask_mongoengine import MongoEngine
from settings import MONGODB_HOST

db = MongoEngine()

def create_app(**config_overrides):

    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    app.config.update(config_overrides)
    db.init_app(app)

    # import blueprints
    from store.views import store_app
    from home.views import home_app
    from pet.views import pet_app
    from app.views import app_app

    # register blueprints
    app.register_blueprint(store_app)
    app.register_blueprint(home_app)
    app.register_blueprint(pet_app)
    app.register_blueprint(app_app)

    return app


def fixtures(test_db, collection, fixture):
    command = "mongoimport -h %s \
        -d %s \
        -c %s \
        < %s" % (MONGODB_HOST, test_db, collection, fixture)
    call(command, shell=True)
