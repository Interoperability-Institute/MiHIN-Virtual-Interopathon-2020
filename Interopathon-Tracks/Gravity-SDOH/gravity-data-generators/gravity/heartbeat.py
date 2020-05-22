from flask import Blueprint, abort, jsonify, request

heartbeat = Blueprint('heartbeat', __name__)

@heartbeat.route('/heartbeat')
def application_heartbeat():
    return 'Application is up and running'