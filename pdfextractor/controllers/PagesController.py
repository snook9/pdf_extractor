# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import os
from flask import redirect, url_for, render_template
from flask import current_app as app
from werkzeug.utils import secure_filename
from pdfextractor.models.ArticleModel import ArticleModel

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
        if request.method == 'POST':
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
                if None == ArticleModel().persist(filename):
                    return redirect(url_for('router.index', message="This file's type is not allowed!"))
                return redirect(url_for('router.index', id=id, message="The file \'" + filename + "\' has been sent successfully!"))
                
            return redirect(url_for('router.index', message="This file's type is not allowed!"))
        else:
            message = request.args.get('message')
            if None == message:
                message = ''

            return render_template('index.html', title="page", message=message)
    
    def getDocument(self, request, id: int):
        if request.method == 'GET':
            # TODO code temporaire
            from sqlalchemy import select
            stmt = select(ArticleModel).where(ArticleModel.id == id)
            from pdfextractor.common.base import session_factory
            session = session_factory()
            result = session.execute(stmt)
            for user_obj in result.scalars():
                print(f"{user_obj.content} {user_obj.datetime}")
            # Fin du code temporaire
            return render_template('index.html', title="page", message=id)