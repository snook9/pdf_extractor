# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

from flask import Blueprint, request

from pdfextractor.controllers.PagesController import PagesController

bp = Blueprint('router', __name__, template_folder='templates')

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/documents', methods=['GET', 'POST'])
def index():
    """Index of the API.
    GET method returns an HTML upload form.
    POST method can be used to upload a PDF file.
        See README.md for response format.

    Returns:
        flask.Response: standard flask HTTP response.
    """
    pagesController = PagesController()
    return pagesController.index(request)

@bp.route('/documents/<int:id>', methods=['GET'])
def getDocument(id):
    """Index of the API.
    GET method returns metadata about the document, specified by the ID parameter.
        See README.md for response format.

    Returns:
        flask.Response: standard flask HTTP response.
    """
    pagesController = PagesController()
    return pagesController.getDocument(request, id)