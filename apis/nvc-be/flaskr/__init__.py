import os
import json

from flask import Flask

from flask_cors import CORS

from flaskr.config import Config

from flaskr.cache import cache

from flasgger import Swagger


def create_app(config=Config):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    from flaskr.blueprints.authenticate import authenticate
    app.register_blueprint(authenticate)

    from flaskr.blueprints.collection import collection
    app.register_blueprint(collection)

    from flaskr.blueprints.wallet import wallet
    app.register_blueprint(wallet)

    swagger = Swagger(app, config={
        "headers": [
        ],
        "title": "NVC API",
        "version": "1.0.0",
        "description": "powered by NVC Global",
        "specs": [
            {
                "endpoint": '/api/apispec_1',
                "route": '/api/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/api/flasgger_static",
        # "static_folder": "/   api/flasgger_static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/api/docs/"
    })

    cache.init_app(app)

    CORS(app, allow_headers=["Content-Type", "Authorization",
         "Access-Control-Allow-Credentials"], origins="*")
    # print(app.config)
    return app
