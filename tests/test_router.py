# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import json

def test_index(client):
    """Test the index route"""
    response = client.get("/")
    assert response.status == "200 OK"
    response = client.get("/documents")
    assert response.status == "200 OK"
    # Test uploading a file
    data = {
        'file': (b"my file contents", "test_file.txt"), # we use StringIO to simulate file object
    }
    response = client.post("/", data=data)
    assert response.status == "200 OK"

def test_get_document(client):
    """Test the /documents/<id> route

    Important: This test can pass if the first line of the database is not empty!
    SO, YOU NEED FIRST TO UPLOAD ONE FILE, AT LEAST, WITH THE APP (started normaly)
    """
    response = client.get("/documents/1")
    data = json.loads(response.get_data(as_text=True))

    # The status must be 200 OK
    assert response.status == "200 OK"
    # We test if we received the ID of the JSON object
    assert data["id"] == 1
