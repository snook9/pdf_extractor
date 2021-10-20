# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import os
from flask import flash, redirect, url_for
from flask import current_app as app
from werkzeug.utils import secure_filename

class PagesController:
    def __allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    def index(request):
        if request.method == 'POST':
            #print(request.form)
            #return b'data received'
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and PagesController.__allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('router.index', filename=filename))
            return b"ERROR"
        else:
            return b"""
            <!doctype html>
            <title>Upload new file</title>
            <h1>Wellcome<h1>
            <h3>Here you will find a zen space, where you can send a file in all serenity.</h3>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
            """