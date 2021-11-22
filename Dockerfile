FROM debian:10

# DEPENDENCIES
RUN apt update -q -y
RUN apt install -yf \
    build-essential libpoppler-cpp-dev pkg-config python3-dev \
    python3 \
    python3-pip

# APP INSTALLATION
COPY ./ /PdfExtractor/
WORKDIR /PdfExtractor/

RUN python3 --version
RUN pip3 install -r requirements.txt \
    && pip3 install '.[test]'

ENV FLASK_APP pdfextractor
ENV FLASK_ENV production
EXPOSE 5000

ENTRYPOINT ["python3", "-m", "flask", "run", "--host=0.0.0.0"]