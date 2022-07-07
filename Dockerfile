FROM python:latest

# install exporter reqs
RUN pip3 install prometheus_client pynetbox environs

COPY main.py /main.py
RUN chmod +x /main.py

CMD ["python3", "main.py"]