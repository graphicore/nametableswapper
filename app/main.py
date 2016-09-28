# [START app]
import logging
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/changenames')
def changenames():
    return 'Hello World'



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
