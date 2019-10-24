from flask import Flask
from config import config

from .extensions import db, LOG

from flask_swagger_ui import get_swaggerui_blueprint

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Approvals"
    }
)
### end swagger specific ###

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

    # swagger ui
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    return app


