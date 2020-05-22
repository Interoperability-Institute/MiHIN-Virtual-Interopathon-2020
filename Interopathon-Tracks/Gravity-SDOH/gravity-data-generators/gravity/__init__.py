import os

from flask import Flask, jsonify, request, abort
from gravity.autoresponder import autoresponder
from gravity.screeningrequest import patientListGenerator
from gravity.researchrequest import researchRequestGenerator
from gravity.heartbeat import heartbeat


def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)

    #if test_config is None:
        # load the instance config, if it exists, when not testing
    #    app.config.from_pyfile('config.py', silent=True)
    #else:
        # load the test config if passed in
    #    app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.register_blueprint(autoresponder)
    app.register_blueprint(patientListGenerator)
    app.register_blueprint(researchRequestGenerator)
    app.register_blueprint(heartbeat)

    return app