# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import pdftotext
from datetime import datetime
from pathlib import Path
from flask import current_app as app
from sqlalchemy import Column, Integer, String
from pdfextractor.common.base import Base
from pdfextractor.common.base import session_factory

class ArticleModel(Base):
    __tablename__ = 'file'
    _id=Column('id', Integer, primary_key=True)
    _content=Column('content', String)
    _datetime=Column('datetime', String(255))
    id=-1

    def __init__(self: object, content: str=None, datetime: str=None):
        self._content = str(content)
        self._datetime = str(datetime)

        self._output_folder = Path(app.config['DATA_FOLDER'])
        if False == self._output_folder.exists():
            self._output_folder.mkdir()

    def _persist(self, content: str, datetime: str):
        session = session_factory()
        self._content = str(content)
        self._datetime = str(datetime)
        session.add(self)
        session.commit()
        self.id = self._id
        session.close()

    def persist(self, filename: str):
        today = datetime.today()
        output_filepath = self._output_folder / Path('file_' + today.strftime("%Y-%m-%d-%H-%M-%S.%f") + '.txt')

        if "pdf" == filename.rsplit('.', 1)[1].lower():
            with open(filename, "rb") as f:
                data = pdftotext.PDF(f)
                with open(output_filepath, 'w') as f:
                    f.write('\n'.join(data))
                    self._persist(''.join(data), output_filepath)
                    return self.id
        return -1