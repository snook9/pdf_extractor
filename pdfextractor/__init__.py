"""
Name: PdfExporter
Authors: Jonathan CASSAING
Tool for parsing and extracting PDF file content
"""

from flask import Flask
from pdfextractor import router


def create_app(test_config=None):
    """Create and configure the flask app with the factory pattern"""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_pyfile("config.py", silent=False)
        app.config.update(test_config)

    # Register the router
    app.register_blueprint(router.bp)

    return app
