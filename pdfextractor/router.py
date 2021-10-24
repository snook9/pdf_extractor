# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

from flask import Blueprint, request

from pdfextractor.controllers.PagesController import PagesController

bp = Blueprint('router', __name__, template_folder='templates')

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/documents', methods=['GET', 'POST'])
def index():
    pagesController = PagesController()
    return pagesController.index(request)