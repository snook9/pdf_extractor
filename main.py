"""
Name: PdfExporter
Authors: Jonathan CASSAING
Tool for parsing and extracting PDF file content
"""

from pdfextractor import create_app

app = create_app()

if __name__ == "__main__":
    print("PdfExtractor v1.0.0")
    print("Server started!")

    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
