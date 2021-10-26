FROM debian:10

# INSTALLATION
RUN apt update \
    && apt install -yf \
    build-essential libpoppler-cpp-dev pkg-config python3-dev \
    python3-pip \
    git

#RUN git clone git@gitlab-student.centralesupelec.fr:jonathan.cassaing/pdfextractor.git
COPY * /PdfExtractor/
WORKDIR /PdfExtractor/
RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt
RUN export FLASK_APP=pdfextractor; \
    export FLASK_ENV=development
RUN flask run

#EXPOSE 80
#EXPOSE 443