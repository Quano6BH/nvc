import os

from flask import Flask

from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

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
    return app
