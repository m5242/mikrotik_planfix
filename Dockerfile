FROM python:3.10.10-slim

ADD main.py .
ADD mikrotik.py .
ADD planfix.py .
ADD config.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]