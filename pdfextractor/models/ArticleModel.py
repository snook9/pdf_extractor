"""
Name: PdfExporter
Authors: Jonathan CASSAING
Tool for parsing and extracting PDF file content
"""

# pdftotext is used to extract PDF content (text body)
import pdftotext
# PyPDF2 is used to extract PDF meta data
from PyPDF2 import PdfFileReader
import json
from datetime import datetime
from pathlib import Path
from flask import current_app as app
from sqlalchemy import Column, Integer, String
from pdfextractor.common.base import Base
from pdfextractor.common.base import session_factory

class ArticleModel(Base):
    """Class for representing Article entity and his Data Access Object

    This class can be used to persist the object in the database AND
    to save the Article in a basic text file. 
    """
    # Table name in the database
    __tablename__ = 'file'
    # ID primary key in the database
    id=Column('id', Integer, primary_key=True)
    # Datetime column in the database
    datetime=Column('datetime', String(255))
    # Author PDF meta data
    author=Column('author', String(255))
    # Creator PDF meta data
    creator=Column('creator', String(255))
    # Producer PDF meta data
    producer=Column('producer', String(255))
    # Subjet PDF meta data
    subject=Column('subject', String(255))
    # Title PDF meta data
    title=Column('title', String(255))
    # Pages count PDF meta data
    number_of_pages=Column('number_of_pages', Integer)
    # Raw informations PDF meta data
    raw_info=Column('raw_info', String())
    # Content column in the database
    content=Column('content', String)
    # Internal ID is used to store the real ID (in database) after the session close
    _internal_id=None

    def __init__(self: object, datetime: str=None, 
                author: str=None,
                creator: str=None,
                producer: str=None,
                subject: str=None,
                title: str=None,
                number_of_pages: int=None,
                raw_info: str=None,
                content: str=None):
        """Initialize the object

        Args:
            datetime (str, optional): to force datetime. Defaults to None.
            author (str, optional): to force author. Defaults to None.
            creator (str, optional): to force creator. Defaults to None.
            producer (str, optional): to force producer. Defaults to None.
            subject (str, optional): to force subject. Defaults to None.
            title (str, optional): to force title. Defaults to None.
            number_of_pages (int, optional): to force number_of_pages. Defaults to None.
            raw_info (str, optional): to force raw_info. Defaults to None.
            content (str, optional): to force content. Defaults to None.
        """
        self.datetime = str(datetime)
        self.author = str(author)
        self.creator = str(creator)
        self.producer = str(producer)
        self.subject = str(subject)
        self.title = str(title)
        self.number_of_pages = number_of_pages
        self.raw_info = str(raw_info)
        self.content = str(content)

        # Configure the folder where text files will be saved
        self._output_folder = Path(app.config['DATA_FOLDER'])
        if False == self._output_folder.exists():
            # If the folder doesn't exist, we create it
            self._output_folder.mkdir()

    def _persist(self, datetime: str, 
                author: str,
                creator: str,
                producer: str,
                subject: str,
                title: str,
                number_of_pages: int,
                raw_info: str,
                content: str):
        """Private method to persist the object in the database

        Args:
            datetime (str): datetime field
            author (str): author field
            creator (str): creator field
            producer (str): producer field
            subject (str): subject field
            title (str): title field
            number_of_pages (int): number_of_pages field
            raw_info (str): raw_info field
            content (str): content field
        """
        session = session_factory()
        self.datetime = str(datetime)
        self.author = str(author)
        self.creator = str(creator)
        self.producer = str(producer)
        self.subject = str(subject)
        self.title = str(title)
        self.number_of_pages = number_of_pages
        self.raw_info = str(raw_info)
        self.content = str(content)
        session.add(self)
        session.commit()
        # We save the ID cause it will wiped after the session.close()
        self._internal_id = self.id
        session.close()

    def persist(self, filename: str):
        """Public method to extract then persist a PDF file content/meta info in the database

        Args:
            filename (str): filename of the target file

        Returns:
            int: ID of the persisted object in the database, otherwise - returns None if the file's type is not supported.
        """
        today = datetime.today().strftime("%Y-%m-%d-%H-%M-%S.%f")
        # Create a unique filename
        output_filepath = self._output_folder / Path('file_' + today + '.txt')

        if "pdf" == filename.rsplit('.', 1)[1].lower():
            with open(filename, "rb") as f:
                # Extracting the text (content)
                data = pdftotext.PDF(f)

                # Extracting meta data
                pdf = PdfFileReader(f)
                info = pdf.getDocumentInfo()
                number_of_pages = pdf.getNumPages()
                author = info.author
                creator = info.creator
                producer = info.producer
                subject = info.subject
                title = info.title

                with open(output_filepath, 'w') as f:
                    # Saving content to a text file
                    f.write('\n'.join(data))
                    # Saving content AND meta data to the database
                    self._persist(today,
                                author,
                                creator,
                                producer,
                                subject,
                                title,
                                number_of_pages,
                                info,
                                ''.join(data))
                    return self._internal_id
        return None

class ArticleEncoder(json.JSONEncoder):
    """Class for converting full object to JSON string
    """
    def default(self, o): 
        if isinstance(o, ArticleModel):
            id = o.id
            if None == id:
                # If None, the object was created after a INSERT query, so, the internal_id is the table id
                id = o._internal_id
            
            return {
                "id": id,
                "datetime": o.datetime,
                "author": o.author,
                "creator": o.creator,
                "producer": o.producer,
                "subject": o.subject,
                "title": o.title,
                "number_of_pages": o.number_of_pages,
                "raw_info": o.raw_info,
                "content" : o.content
                } 
        else:
            # Base class will raise the TypeError.
            return super().default(o)