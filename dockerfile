FROM python:3

EXPOSE 6677

WORKDIR /opt/asyncxmlrpc
COPY /asyncxmlrpc/ .

CMD ["python3", "serve_forever.py"]