# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

def test_index(client):
    response = client.get("/")
    assert response.data == b"""
            <!doctype html>
            <title>Upload new file</title>
            <h1>Wellcome<h1>
            <h3>Here you will find a zen space, where you can send a file in all serenity.</h3>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
            """

def test_index_post(client):
    response = client.post("/")
    assert response.data == b"data received"
