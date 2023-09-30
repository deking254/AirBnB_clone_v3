#!/usr/bin/python3
"""a functon to get status of API"""
import os
from models import storage
from flask.app import Flask
from flask import make_response, jsonify
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def handle_teardown(exception):
    """handle @app.teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    data = {"error": "Not found"}
    return jsonify(data), 404


if __name__ == "__main__":
    hst = os.getenv('HBNB_API_HOST')
    prt = os.getenv('HBNB_API_PORT')
    if hst and prt:
        app.run(host=hst, port=prt, threaded=True)
    else:
        app.run(host='0.0.0.0', port='5000', threaded=True)
