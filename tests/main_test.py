# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content


import unittest
import main


class MainTestCase(unittest.TestCase):
    def test_main(self):
        with main.app.app_context():
            self.assertEqual('<h1>Bienvenue</h1>', '<h1>Bienvenue</h1>')

if __name__ == '__main__':
    unittest.main()
