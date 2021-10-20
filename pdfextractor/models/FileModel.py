# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import pdftotext
from pathlib import Path

class FileModel:
    def __init__(self: object):
        self._output_folder = Path("data")
        if False == self._output_folder.exists():
            self._output_folder.mkdir()
        pass

    def persist(self, filename):
        if "pdf" == filename.rsplit('.', 1)[1].lower():
            with open(filename, "rb") as f:
                file = pdftotext.PDF(f)
        
        filepath = self._output_folder / Path(filename + '.txt')

        with open(filepath, 'w') as f:
            f.write('\n'.join(file))
