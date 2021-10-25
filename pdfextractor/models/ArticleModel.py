# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import pdftotext
import json
from datetime import datetime
from pathlib import Path
from flask import current_app as app
from sqlalchemy import Column, Integer, String
from pdfextractor.common.base import Base
from pdfextractor.common.base import session_factory

class ArticleModel(Base):
    __tablename__ = 'file'
    id=Column('id', Integer, primary_key=True)
    datetime=Column('datetime', String(255))
    content=Column('content', String)
    # Internal ID is used to store the real ID (in database) after the session close
    _internal_id=None

    def __init__(self: object, datetime: str=None, content: str=None):
        self.datetime = str(datetime)
        self.content = str(content)

        self._output_folder = Path(app.config['DATA_FOLDER'])
        if False == self._output_folder.exists():
            self._output_folder.mkdir()

    def _persist(self, datetime: str, content: str):
        session = session_factory()
        self.datetime = str(datetime)
        self.content = str(content)
        session.add(self)
        session.commit()
        # We save the ID cause it will wiped after the session.close()
        self._internal_id = self.id
        session.close()

    def persist(self, filename: str):
        today = datetime.today().strftime("%Y-%m-%d-%H-%M-%S.%f")
        output_filepath = self._output_folder / Path('file_' + today + '.txt')

        if "pdf" == filename.rsplit('.', 1)[1].lower():
            with open(filename, "rb") as f:
                data = pdftotext.PDF(f)
                with open(output_filepath, 'w') as f:
                    f.write('\n'.join(data))
                    self._persist(today, ''.join(data))
                    return self._internal_id
        return None

class ArticleEncoder(json.JSONEncoder):
    def default(self, o): 
        if isinstance(o, ArticleModel):
            id = o.id
            if None == id:
                # If None, the object was created after a INSERT query, so, the internal_id is the table id
                id = o._internal_id
            
            return {
                "id": id,
                "datetime": o.datetime,
                "content" : o.content
                } 
        else:
            # Base class will raise the TypeError.
            return super().default(o)