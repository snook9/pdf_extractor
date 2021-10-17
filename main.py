# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content


import config
from flask import Flask
from flask import request


config = config.configure()
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        request.form
    else:
        output = '<h1>Bienvenue</h1>'
    
    return output
