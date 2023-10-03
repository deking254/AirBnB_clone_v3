#!/usr/bin/python3
"""a function to get the status of the API"""
import os
from models import storage
from flask import Flask, jsonify
from flask_cors import CORS  
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

# Configure CORS to allow requests from all origins for all API routes
CORS(app)

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
    if not hst:
        hst = '0.0.0.0'
    if not prt:
        prt = '5000'
    app.run(host=hst, port=prt, threaded=True)