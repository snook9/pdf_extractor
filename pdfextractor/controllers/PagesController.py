# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import os
from flask import redirect, url_for, render_template
from flask import current_app as app
from werkzeug.utils import secure_filename

class PagesController:
    def _allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    def index(request):
        if request.method == 'POST':
            #print(request.form)
            #return b'data received'
            # check if the post request has the file part
            if 'file' not in request.files:
                #flash('No file part')
                return redirect(url_for('router.index', message="No file part"))
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                #flash('No selected file')
                return redirect(url_for('router.index', message="No selected file"))
            if file and PagesController._allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('router.index', message="The file \'" + filename + "\' has been sent successfully!"))
            return redirect(url_for('router.index', message="This file's type is not allowed!"))
        else:
            message = request.args.get('message')
            if None == message:
                message = ''

            return render_template('index.html', title="page", message=message)