"""
Name: PdfExporter
Authors: Jonathan CASSAING
Tool for parsing and extracting PDF file content
"""

from flask import Blueprint, request

from pdfextractor.controllers.ApiController import ApiController

bp = Blueprint("router", __name__, template_folder="templates")


@bp.route("/", methods=["GET", "POST"])
@bp.route("/documents", methods=["GET", "POST"])
def index():
    """Index of the API.
    GET method returns an HTML upload form.
    POST method can be used to upload a PDF file.
        See README.md for response format.

    Returns:
        flask.Response: standard flask HTTP response.
    """
    api_controller = ApiController()
    return api_controller.index(request)


@bp.route("/documents/<int:doc_id>", methods=["GET"])
def get_document(doc_id):
    """Information about a document.
    GET method returns metadata about the document, specified by the ID parameter.
        See README.md for response format.

    Returns:
        flask.Response: standard flask HTTP response.
    """
    return ApiController.get_document(request, doc_id)


@bp.route("/text/<int:doc_id>", methods=["GET"])
def get_text(doc_id):
    """Content of a document.
    GET method returns the content of a document, specified by the ID parameter.
        See README.md for response format.

    Returns:
        flask.Response: standard flask HTTP response.
    """
    return ApiController.get_text(request, doc_id)
