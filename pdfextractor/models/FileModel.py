# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import pdftotext
from datetime import datetime
from pathlib import Path
from flask import current_app as app
from shutil import copyfile
from sqlalchemy import Column, Integer, String
from pdfextractor.common.base import Base
from pdfextractor.common.base import session_factory

class FileModel(Base):
    __tablename__ = 'file'
    id=Column(Integer, primary_key=True)
    content=Column('content', String())
    datetime=Column('datetime', String(255))

    def __init__(self: object, content=None, datetime=None):
        self.content = content
        self.datetime = datetime

        self._output_folder = Path(app.config['DATA_FOLDER'])
        if False == self._output_folder.exists():
            self._output_folder.mkdir()

    def persist(self, filename: str):
        today = datetime.today()
        output_filepath = self._output_folder / Path('file_' + today.strftime("%Y-%m-%d-%H-%M-%S.%f") + '.txt')

        if "pdf" == filename.rsplit('.', 1)[1].lower():
            with open(filename, "rb") as f:
                data = pdftotext.PDF(f)
                with open(output_filepath, 'w') as f:
                    f.write('\n'.join(data))
        elif "txt" == filename.rsplit('.', 1)[1].lower():
            copyfile(filename, output_filepath)
            session = session_factory()
            self.content = "JoeJoe"
            self.datetime = "09/04/1988"
            session.add(self)
            session.commit()
            session.close()