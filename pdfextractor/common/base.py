"""
Name: PdfExporter
Authors: Jonathan CASSAING
Tool for parsing and extracting PDF file content
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///instance/pdfextractor.db')
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()

def session_factory():
    """Returns a session factory to simplify database access
    """
    Base.metadata.create_all(engine)
    return _SessionFactory()
