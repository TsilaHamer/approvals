from flask import Flask
from config import config

from .extensions import db, LOG


def create_app(config_name='production', name=None):
    """ Creates an application instance """
    app = Flask(__name__)
    if name:
        app.name = name
    # import configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initializes extensions
    db.init_app(app)

    # import blueprints
    from .approval_api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    # app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app



