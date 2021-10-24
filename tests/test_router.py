# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

def test_index(client):
    """Test the index route
    """
    response = client.get("/")
    assert response.status == '200 OK'
    response = client.get("/documents")
    assert response.status == '200 OK'
    response = client.post("/")
    assert response.status == '302 FOUND'