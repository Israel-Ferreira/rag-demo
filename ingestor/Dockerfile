FROM python:3.10 

WORKDIR /usr/src/ingestor

COPY requirements.txt /usr/src/ingestor/

RUN pip install -r requirements.txt

COPY . /usr/src/ingestor/

CMD ["python", "/usr/src/ingestor/main.py"]
