# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

from flask import Flask
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

from pdfextractor.models.FileModel import FileModel

def create_db():
    engine = create_engine('sqlite:///instance/pdfextractor.db', echo = True)
    meta = MetaData()

    files = FileModel.getTable(meta)

    meta.create_all(engine)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_pyfile('config.py', silent=False)
        app.config.update(test_config)

    create_db()

    from pdfextractor import router
    app.register_blueprint(router.bp)

    return app