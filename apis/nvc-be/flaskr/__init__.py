import os
import json

from flask import Flask

from flask_cors import CORS

from flaskr.config import Config



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

    CORS(app, allow_headers=["Content-Type", "Authorization",
         "Access-Control-Allow-Credentials"], origins="*")
    # print(app.config)
    return app
