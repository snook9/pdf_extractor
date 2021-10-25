# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import os
import json
from flask import Response, render_template
from flask import current_app as app
from werkzeug.utils import secure_filename
from pdfextractor.models.ArticleModel import ArticleEncoder, ArticleModel
from pdfextractor.models.MessageModel import MessageEncoder, MessageModel
from pdfextractor.common.base import session_factory
from sqlalchemy import select

from pdfextractor.models.MessageModel import MessageModel

class PagesController:
    def __init__(self: object):
        pass

    @staticmethod
    def _allowed_file(filename: str):
        """Check is the file extension is allowed according to the config.cfg file.

        Args:
            filename (str): file to check.

        Returns:
            bool: True if the extension of the filename is allowed, otherwise - returns False.
        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    def index(self, request):
        """Index of the API.
        GET method returns an HTML upload form.
        POST method can be used to upload a PDF file.
            See README.md for response format.

        Returns:
            flask.Response: standard flask HTTP response.
        """
        # If it's a POST request (the client try to send a file)
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                return Response(json.dumps(MessageModel("No file part"), cls=MessageEncoder), mimetype='application/json;charset=utf-8')

            # Else, we get the file
            file = request.files['file']

            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return Response(json.dumps(MessageModel("No selected file"), cls=MessageEncoder), mimetype='application/json;charset=utf-8')

            # If the file's type is allowed
            if file and PagesController._allowed_file(file.filename):
                # Check user input
                filename = secure_filename(file.filename)
                # Save the file in an upload folder
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Persist the file in the database
                id = ArticleModel().persist(filename)
                # If failed
                if None == id:
                    # Returns the appropriate error
                    return Response(json.dumps(MessageModel("This file's type is not allowed!"), cls=MessageEncoder), mimetype='application/json;charset=utf-8')
                # Else, returning the ID of the object in the database
                return Response(json.dumps(MessageModel("The file \'" + filename + "\' has been sent successfully!", id), cls=MessageEncoder), mimetype='application/json;charset=utf-8')

            # Else, the file's type is not allowed
            return Response(json.dumps(MessageModel("This file's type is not allowed!"), cls=MessageEncoder), mimetype='application/json;charset=utf-8')
        else:
            # Check if the application returns a message
            # NO MORE USED CURRENTLY
            message = request.args.get('message')
            if None == message:
                message = ''

            # Generate an index HTML page with an outstanding look & feel
            return render_template('index.html', title="page", message=message)
    
    def getDocument(self, request, id: int):
        """Index of the API.
        GET method returns metadata about the document, specified by the ID parameter.
            See README.md for response format.

        Returns:
            flask.Response: standard flask HTTP response.
        """
        if request.method == 'GET':
            # Preparing the query for the ID
            stmt = select(ArticleModel).where(ArticleModel.id == id)
            # Retreive the session
            session = session_factory()
            # Executing the query
            result = session.execute(stmt)
            json_data = None
            # Parsing the result
            for user_obj in result.scalars():
                # Converting the object to JSON string
                json_data = json.dumps(user_obj, cls=ArticleEncoder)
                # We leave the for and return the first element (cause "normaly", there is only one row)
                return Response(json_data, mimetype='application/json;charset=utf-8')
            # Else, no document found
            return Response(json.dumps(MessageModel("No document found"), cls=MessageEncoder), mimetype='application/json;charset=utf-8')