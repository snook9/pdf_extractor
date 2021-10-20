# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import unittest
import pdfextractor.controllers.PagesController as PagesController
from pdfextractor import create_app

class test_PagesController(unittest.TestCase):
    def test_allowed_file(self):
        with create_app({"TESTING": True}).app_context():
            result = PagesController.PagesController()._allowed_file('file.pdf')
            self.assertEqual(50, 50)