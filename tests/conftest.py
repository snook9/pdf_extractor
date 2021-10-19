# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import pytest

from pdfextractor import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app({"TESTING": True})

    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
