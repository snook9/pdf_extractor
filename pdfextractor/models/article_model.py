"""
Name: PdfExporter
Authors: Jonathan CASSAING
Tool for parsing and extracting PDF file content
"""

from datetime import datetime
from pathlib import Path
import json
# pdftotext is used to extract PDF content (text body)
import pdftotext
# PyPDF2 is used to extract PDF meta data
from PyPDF2 import PdfFileReader
from flask import current_app as app
from sqlalchemy import Column, Integer, String
from pdfextractor.common.base import Base
from pdfextractor.common.base import session_factory
from multiprocessing import Process

class ArticleModel(Base):
    """Class for representing Article entity and his Data Access Object

    This class can be used to persist the object in the database AND
    to save the Article in a basic text file.
    """

    # Table name in the database
    __tablename__ = "file"
    # Internal ID is used to store the real ID (in database) after the session close
    internal_id = None
    # ID primary key in the database
    # Nota: this id is wiped after a session.close()
    id = Column("id", Integer, primary_key=True)
    # Status column in the database
    status = Column("status", String(255))
    # Date and time column in the database
    date = Column("date", String(255))
    # Author PDF meta data
    author = Column("author", String(255))
    # Creator PDF meta data
    creator = Column("creator", String(255))
    # Producer PDF meta data
    producer = Column("producer", String(255))
    # Subjet PDF meta data
    subject = Column("subject", String(255))
    # Title PDF meta data
    title = Column("title", String(255))
    # Pages count PDF meta data
    number_of_pages = Column("number_of_pages", Integer)
    # Raw informations PDF meta data
    raw_info = Column("raw_info", String())
    # Content column in the database
    content = Column("content", String)

    def __init__(
        self: object,
        status: str = None,
        date: str = None,
        author: str = None,
        creator: str = None,
        producer: str = None,
        subject: str = None,
        title: str = None,
        number_of_pages: int = None,
        raw_info: str = None,
        content: str = None,
    ):
        """Initialize the object

        Args:
            status (str, optional): to force status. Defaults to None.
            date (str, optional): to force date and time. Defaults to None.
            author (str, optional): to force author. Defaults to None.
            creator (str, optional): to force creator. Defaults to None.
            producer (str, optional): to force producer. Defaults to None.
            subject (str, optional): to force subject. Defaults to None.
            title (str, optional): to force title. Defaults to None.
            number_of_pages (int, optional): to force number_of_pages. Defaults to None.
            raw_info (str, optional): to force raw_info. Defaults to None.
            content (str, optional): to force content. Defaults to None.
        """
        self.status = str(status)
        self.date = str(date)
        self.author = str(author)
        self.creator = str(creator)
        self.producer = str(producer)
        self.subject = str(subject)
        self.title = str(title)
        self.number_of_pages = number_of_pages
        self.raw_info = str(raw_info)
        self.content = str(content)

        # Configure the folder where text files will be saved
        self._output_folder = Path(app.config["DATA_FOLDER"])
        if False is self._output_folder.exists():
            # If the folder doesn't exist, we create it
            self._output_folder.mkdir()

    def _persist(
        self,
        date: str = None,
        author: str = None,
        creator: str = None,
        producer: str = None,
        subject: str = None,
        title: str = None,
        number_of_pages: int = None,
        raw_info: str = None,
        content: str = None,
        id: int = None,
    ):
        """Private method to persist/update the object in the database

        Args:
            date (str): date field
            author (str): author field
            creator (str): creator field
            producer (str): producer field
            subject (str): subject field
            title (str): title field
            number_of_pages (int): number_of_pages field
            raw_info (str): raw_info field
            content (str): content field
            id (int): none for inserting a new object, otherwise - id of the object to update
        """
        session = session_factory()
        if None == id:
            self.status = "PENDING"
            self.date = str(date)
            self.author = str(author)
            self.creator = str(creator)
            self.producer = str(producer)
            self.subject = str(subject)
            self.title = str(title)
            self.number_of_pages = number_of_pages
            self.raw_info = str(raw_info)
            self.content = str(content)
            session.add(self)
        else:
            article_model = session.query(ArticleModel).get(id)
            article_model.status = "SUCCESS"
            article_model.date = str(date)
            article_model.author = str(author)
            article_model.creator = str(creator)
            article_model.producer = str(producer)
            article_model.subject = str(subject)
            article_model.title = str(title)
            article_model.number_of_pages = number_of_pages
            article_model.raw_info = str(raw_info)
            article_model.content = str(content)

        session.commit()
        # We save the ID cause it will wiped after the session.close()
        self.internal_id = self.id
        session.close()   

        return self.internal_id

    def _async_extract_and_persist(self, filename: Path, id: int):
        """Private method to extract then update a PDF object in the database
        You must use persist() without parameter before, to get the id of your futur line in the database

        Args:
            filename (str): filename of the target file
            id (int): id of the database line to update

        Returns:
            int: ID of the persisted object in the database.
        """
        today = datetime.today().strftime("%Y-%m-%d-%H-%M-%S.%f")
        # Create a unique filename
        output_filepath = self._output_folder / Path("file_" + today + ".txt")

        with open(filename, "rb") as file:
            # Extracting the text (content)
            data = pdftotext.PDF(file)

            # Extracting meta data
            pdf = PdfFileReader(file)
            info = pdf.getDocumentInfo()
            number_of_pages = pdf.getNumPages()
            author = info.author
            creator = info.creator
            producer = info.producer
            subject = info.subject
            title = info.title

            with open(output_filepath, "w", encoding="utf-8") as file:
                # Saving content to a text file
                file.write("\n".join(data))
                # Saving content AND meta data to the database
                self._persist(
                    today,
                    author,
                    creator,
                    producer,
                    subject,
                    title,
                    number_of_pages,
                    info,
                    "".join(data),
                    id
                )
                return self.internal_id

    def extract_and_persist(self, filename: Path):
        """Public method to extract then persist a PDF object in the database
        First, this method ask an ID for the futur line in the database, then,
        this method create a process for extracting data and persisting the object in the database.
        This method returns the ID of the object in the database which will be inserted when the process will finish.

        Args:
            filename (str): filename of the target file

        Returns:
            int: ID of the persisted object in the database,
            otherwise - returns None if the file's type is not supported.
        """
        if str(filename).rsplit(".", 1)[1].lower() == "pdf":
            # We persist an empty object just to get the ID of the line in the database
            id = self._persist()

            process = Process(target=self._async_extract_and_persist, args=(filename, id))
            process.start()

            return id

        return None

class ArticleEncoder(json.JSONEncoder):
    """Class for converting full object to JSON string"""

    def default(self, o):
        if isinstance(o, ArticleModel):
            doc_id = o.id
            if None is doc_id:
                # If None, the object was created after a INSERT query,
                # so, the internal_id is the table id
                doc_id = o.internal_id

            return {
                "id": doc_id,
                "status": o.status,
                "date": o.date,
                "author": o.author,
                "creator": o.creator,
                "producer": o.producer,
                "subject": o.subject,
                "title": o.title,
                "number_of_pages": o.number_of_pages,
                "raw_info": o.raw_info,
                "content": o.content,
            }
        # Base class will raise the TypeError.
        return super().default(o)
