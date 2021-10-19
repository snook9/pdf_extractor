# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

def test_index(client):
    response = client.get("/")
    assert response.data == b"<h1>Bienvenue</h1>"
