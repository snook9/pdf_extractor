# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import unittest
import pdfextractor.controllers.ApiController as ApiController
from pdfextractor import create_app

class test_ApiController(unittest.TestCase):
    def test_allowed_file(self):
        """Test different file types
        """
        with create_app({"TESTING": True}).app_context():
            # Must be OK for PDF file type
            self.assertTrue(ApiController.ApiController()._allowed_file('file.pdf'))
            # Must be False for other file types
            self.assertFalse(ApiController.ApiController()._allowed_file('file.txt'))