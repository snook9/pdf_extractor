# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import unittest
import pdfextractor.controllers.PagesController as PagesController

class test_PagesController(unittest.TestCase):

    pageController = PagesController.PagesController()

    def test_allowed_file(self):
        result = self.pageController._allowed_file('file.pdf')
        self.assertEqual(50, 50)  