FROM python:3

EXPOSE 6677

WORKDIR /usr/compare_xmlrpc
ADD /compare_xmlrpc/ .

CMD ["python3", "serve_forever.py"]