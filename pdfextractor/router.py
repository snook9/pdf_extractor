# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

from flask import Blueprint, request

bp = Blueprint('router', __name__, template_folder='templates')

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        output = 'data received'
    else:
        output = '<h1>Bienvenue</h1>'
    
    return output