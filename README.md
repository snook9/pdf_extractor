# PdfExtractor

Tool for parsing and extracting PDF file content.

## Install

### OS Dependencies

These instructions assume you're using Python 3 on a recent OS. Package names may differ for Python 2 or for an older OS.

#### Debian, Ubuntu, and friends

    sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev

#### Fedora, Red Hat, and friends

    sudo yum install gcc-c++ pkgconfig poppler-cpp-devel python3-devel

#### macOS
    
    brew install pkg-config poppler python

#### Windows

Currently tested only when using conda:

- Install the Microsoft Visual C++ Build Tools
- Install poppler through conda:

    conda install -c conda-forge poppler

### PdfExtractor

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
    
    $ curl -F 'file=@article.pdf' localhost:5000

The posted files will be stored in the 'data' directory, according to the 'config.cfg' file.

## Test

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
