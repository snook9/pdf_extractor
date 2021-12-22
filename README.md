# PdfExtractor

Tool for parsing and extracting PDF file content.
This sofware is a RESTful/JSON API which offers the following features:
- upload a PDF file,
  - extract PDF content and meta data,
  - store the PDF content and meta data in a database,
  - save the PDF content in a text file,
- retreive the PDF meta data,
- retreive the PDF content.

# Install

## With Docker

    $ sudo docker build -t pdfextractor .

## With Linux or Mac OS

### Dependencies: pdftotext

These instructions assume you're using Python 3 on a recent OS. Package names may differ for Python 2 or for an older OS.

#### Debian, Ubuntu, and friends

    $ sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev

#### Fedora, Red Hat, and friends

    $ sudo yum install gcc-c++ pkgconfig poppler-cpp-devel python3-devel

#### macOS
    
    $ brew install pkg-config poppler python

### PdfExtractor

Create a virtualenv and activate it:

    $ python -m venv venv
    $ . venv/bin/activate

Install PdfExtractor:

    $ pip install -r requirements.txt

## With Windows OS

Sorry, this app is not currently compatible with Windows... Please use Docker instead

# Run

## With Docker

    $ sudo docker run -d -p 5000:5000 pdfextractor

## With Linux or Mac OS

    $ export FLASK_APP=pdfextractor
    $ export FLASK_ENV=development
    $ flask run

# Usage

Open http://localhost:5000 in a browser to try the software or use the following API.

## API specification

### Upload a file

Post a file to the server:

**Request**

    HTTP Methode: POST
    Route: /
    Alternate: /documents

**Response**

    {
        # ID of the uploaded PDF file, otherwise 'null' if error (int)
        "id": [id],
        # Explicit human readable status message (str)
        "message": "[message]"}"
    }

**Example:**
    
    $ curl -F 'file=@article.pdf' localhost:5000

The posted files will be saved in the 'data' directory, in a raw text file, according to the 'config.cfg' file.

The origin PDF file is temporary stored in the 'uploads' directory, according to the 'config.cfg' file.

### Check an uploaded file

Get the status of an uploaded file and show his meta data:

**Request**

    HTTP Methode: GET
    Route: /documents/{id}
    # Replace the {id} pattern by the target ID of the document
    # The ID was returned in response of an upload file request

**Response**

    {
        # ID of the uploaded PDF file, otherwise 'null' if not found (int)
        # Important: when the id is null, the other fields are not provided and
        # a generic "message" json field give an explicit human readable message (see below)
        "id": [id], 
        # May be "SUCCESS", "PENDING" or "ERROR" (str)
        "status": "[status]",
        # Date and time when the file was uploaded, format "2021-10-26-13-42-01.496144" (str)
        "uploaded_date": "[date]",
        # Author specified in the PDF file as meta data (str)
        "author": "[author]",
        # Creator specified in the PDF file as meta data (str)
        "creator": "[creator]",
        # Producer specified in the PDF file as meta data (str)
        "producer": "[producer]",
        # Subject specified in the PDF file as meta data (str)
        "subject": "[subject]", 
        # Title specified in the PDF file as meta data (str)
        "title": "[title]", 
        # Nomber of pages in the PDF file (int)
        "number_of_pages": [number_of_pages], 
        # Additional information in the PDF file as meta data (str)
        "raw_info": "[raw_info]"
    }

In case of **error** not linked with the PDF file, the following response is returned:

    {
        "id": null,
        # Explicit human readable error message (str)
        "message": "[message]"
    }

### Text of an uploaded file

Get the text (content) of an uploaded file:

**Request**

    HTTP Methode: GET
    Route: /text/{id}
    # Replace the {id} pattern by the target ID of the document
    # The ID was returned in response of an upload file request

**Response**

    {
        # Content of the specified PDF document (str)
        "content": [content]
    }

In case of **error**, the following response is returned:

    {
        "id": null,
        # Explicit human readable error message (str)
        "message": "[message]"
    }

# Test

## pylint

    $ apt install pylint
    $ export PYTHONPATH="venv/lib/python3.9/site-packages/"
    $ pylint --disable too-many-instance-attributes --disable too-few-public-methods --disable too-many-arguments --disable c-extension-no-member pdfextractor/*

## pytest

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ export PYTHONPATH="venv/lib/python3.9/site-packages/"
    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
