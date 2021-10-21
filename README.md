# PdfExtractor

Tool for parsing and extracting PDF file content.

## Install

Create a virtualenv and activate it:

    $ python3 -m venv venv
    $ . venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Install PdfExtractor:

    $ pip install -e .

## Run

    $ export FLASK_APP=pdfextractor
    $ export FLASK_ENV=development
    $ flask run

Or on Windows cmd::

    > set FLASK_APP=pdfextractor
    > set FLASK_ENV=development
    > flask run

Open http://127.0.0.1:5000 in a browser.
Post a file to the server :
    
    $ curl -F 'file=@tests/article.pdf' localhost:5000

The posted files will be stored in the 'data' directory, according to the 'config.cfg' file.

## Test

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
