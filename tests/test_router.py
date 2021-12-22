# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import json
import time

from sqlalchemy.sql.expression import null
from pdfextractor.models.article_model import ArticleModel
from pdfextractor import create_app

def test_index(client):
    """Test the index route"""
    response = client.get("/")
    assert response.status_code == 200
    response = client.get("/documents")
    assert response.status_code == 200

    # Test uploading a file with a forbidden extension
    data = {
        'file': (b"my file contents", "test_file.txt"),
    }
    response = client.post("/", data=data)
    assert response.status_code == 400

def test_get_document(client):
    """Test the /documents/<id> route"""
    # To insert a first document in the database (in case the db is empty)
    with create_app({"TESTING": True}).app_context():
        ArticleModel().extract_and_persist("tests/article.pdf")

    # Now, the first document exists
    # So, we get it
    response = client.get("/documents/1")
    data = json.loads(response.get_data(as_text=True))

    # The status must be 200 OK
    assert response.status_code == 200
    # We test if we received the ID of the JSON object
    assert data["id"] == 1

def test_get_text(client):
    """Test the /text/<id> route"""
    # To insert a first document in the database (in case the db is empty)
    with create_app({"TESTING": True}).app_context():
        ArticleModel().extract_and_persist("tests/article.pdf")

    # Now, the first document exists
    # So, we get it
    response = client.get("/text/1")
    data = json.loads(response.get_data(as_text=True))

    # The status must be 200 OK
    assert response.status_code == 200
    # We test if we received the content of the PDF
    assert data["content"] is not None
