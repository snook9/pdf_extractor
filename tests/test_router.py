# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

def test_index(client):
    response = client.get("/")
    assert response.status == '200 OK'

def test_index_post(client):
    response = client.post("/")
    assert response.status == '302 FOUND'