# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import unittest
import pdfextractor.controllers.PagesController as PagesController
from pdfextractor import create_app

class test_PagesController(unittest.TestCase):
    def test_allowed_file(self):
        """Test different file types
        """
        with create_app({"TESTING": True}).app_context():
            # Must be OK for PDF file type
            self.assertTrue(PagesController.PagesController()._allowed_file('file.pdf'))
            # Must be False for other file types
            self.assertFalse(PagesController.PagesController()._allowed_file('file.txt'))