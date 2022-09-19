FROM python:3.10.7-alpine3.16
WORKDIR /opt/
COPY . .
RUN pip install -r reqs.txt
CMD ["python3", "main.py"]