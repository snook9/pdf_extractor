FROM debian:10

# DEPENDENCIES
RUN apt update -q -y
RUN apt install -yf \
    build-essential libpoppler-cpp-dev pkg-config python3-dev \
    python3 \
    python3-pip \
    git

# APP INSTALLATION
COPY * /PdfExtractor/
WORKDIR /PdfExtractor/

RUN python3 --version
RUN pip3 install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install '.[test]'

# APP
RUN export FLASK_APP=pdfextractor \
    export FLASK_ENV=development

ENTRYPOINT ["flask run"]
