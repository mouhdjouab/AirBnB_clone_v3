#!/usr/bin/python3
"""
Flask app
"""

from models import storage
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def tear_down(self):
    '''API status'''
    storage.close()

@app.errorhandler(404)
def page_not_foun(error):
    """Method that handles 404 status in JSON fromat"""
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host, int(port), threaded=True)

